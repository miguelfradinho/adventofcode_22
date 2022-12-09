from dataclasses import dataclass
from typing import Optional, IO
from collections import deque

@dataclass
class File:
    name : str
    size : int


class Dir:
    def __init__(self, name: str, parent : "Dir" = None):
        # name of this node
        self._name: str = name
        if parent is not None:
            self._parent : Dir = parent
        # right nodes
        self._files: list[File] = list()
        # left nodes
        self._dirs: list[Dir] = list()

        # cache for total size
        self._total_size : Optional[int] = None
        # helper for caching the size
        self._child_changed : bool = True

    @property
    def name(self):
        return self._name
    @property
    def files(self):
        return self._files

    @property
    def dirs(self):
        return self._dirs

    @property
    def parent(self):
        return self._parent

    @property
    def get_size(self):
        # we already calculated, so no need to calculate again
        if not self._child_changed:
            return self._total_size

        curr_size = 0
        # get all the sizes for the files
        for f in self._files:
            curr_size += f.size

        # get the size for all the directories
        for d in self._dirs:
            curr_size += d.get_size

        # we calculated the size, so, update the variables
        self._child_changed = False
        self._total_size = curr_size
        return curr_size

    def add_file(self, file: File):
        self._files.append(file)

    def add_subdirectory(self, sub_dir):
        self._dirs.append(sub_dir)

    def find_child(self, name: str) -> Optional["Dir"]:
        for i in self._dirs:
            if i.name == name:
                return i
        return None

    def __repr__(self):
        return f"({self.name}, dirs={str(self._dirs)}, files={str(self._files)})"

def create_tree(file_obj):
    # create the root node
    ROOT_NODE = Dir("/")
    all_dirs = [ROOT_NODE]
    curr_node: Dir = None
    # we could read directly off the file object
    # however, since this implementation doesn't parse the input the first time
    # we'll need some sort of buffer to handle this
    # (or we could also do low level magic with file seek offsets... but high level is more fun)
    # So, we use lists, which is the simplest way to use as a buffer
    raw_lines = deque(i.strip("\n") for i in file_obj.readlines())
    file_lines = deque(raw_lines)

    has_next = True

    while has_next:
        try:
            # read next line
            line = file_lines.popleft()
        except IndexError:
            has_next = False
            continue
        # we reached end of file
        if line == "":
            break

        # check which command
        match line.lstrip("$ ").split(" "):
            # change command
            case ["cd", dir_name]:
                match dir_name:
                    # move one up
                    case "..":
                        curr_node = curr_node.parent
                        continue
                    # switch to the root
                    case "/":
                        curr_node = ROOT_NODE
                        continue
                    # switch to a subdirectory
                    case dir_name:
                        sub_dir = curr_node.find_child(dir_name)
                        if sub_dir is None:
                            raise ValueError(f"Error parsing, directory {dir_name} was not created")
                        curr_node = sub_dir
                        continue
            # listing
            case ["ls"]:
                # it's a list, so we need to read until the next command
                listed_files = []

                while True:
                    try:
                        next_line = file_lines.popleft()
                    # EOF
                    except IndexError:
                        break

                    # next line is a command, so return it to the buffer
                    if next_line.startswith("$"):
                        file_lines.appendleft(next_line)
                        break
                    # it doesn't start with a command, so it's one of the listed files
                    listed_files.append(next_line)

                # okay, we read all the listed_files so, create it appropriately
                for i in listed_files:
                    dir_or_size, name = i.split(" ")
                    dir_or_size: str
                    # it's a directory, so create it
                    if dir_or_size.startswith("dir"):
                        new_node = Dir(name, curr_node)
                        curr_node.add_subdirectory(new_node)
                        all_dirs.append(new_node)
                    # it's a file
                    else:
                        new_node = File(name, int(dir_or_size))
                        curr_node.add_file(new_node)

    return ROOT_NODE, all_dirs

def day_7(file_obj: IO):
    #example = open("sol_snake\example_7.txt")
    # read the lines while also removing line breaks
    tree, all_dirs = create_tree(file_obj)
    MAX_SIZE = 100_000
    TOTAL_SPACE = 70_000_000
    NEEDED_SPACE = 30_000_000
    UNUSED_SPACE = TOTAL_SPACE - tree.get_size
    THRESHOLD = NEEDED_SPACE-UNUSED_SPACE

    max_size_dirs = []
    possible_to_delete = []
    for d in all_dirs:
        dir_size = d.get_size
        if dir_size <= MAX_SIZE:
            max_size_dirs.append(d)
        if dir_size >= THRESHOLD:
            possible_to_delete.append(d)

    return sum([i.get_size for i in max_size_dirs]),min([i.get_size for i in possible_to_delete])