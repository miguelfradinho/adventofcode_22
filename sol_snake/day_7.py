from dataclasses import dataclass
from typing import Optional, Any
from collections import deque
from enum import StrEnum


class SpecialDir(StrEnum):
    ROOT = "/"
    PARENT = ".."


class CommandType(StrEnum):
    ListFiles = "ls"
    ChangeDir = "cd"

@dataclass
class Command:
    cmd_type: CommandType


class ListFiles(Command):
    result : list
    def __init__(self):
        super().__init__(CommandType.ListFiles)
        self.result = list()

class ChangeDir (Command):
    cmd_arg: Optional[str | SpecialDir]
    def __init__(self, cmd_arg = None):
        super().__init__(CommandType.ChangeDir)
        self.cmd_arg = cmd_arg
@dataclass
class BaseEntity:
    name: str

class File(BaseEntity):
    total_size : int
    def __init__(self, name, total_size):
        super().__init__(name)
        self.total_size = total_size

class Dir(BaseEntity):
    children: list[BaseEntity]
    _total_size: Optional[int]
    _child_changed: bool

    def __init__(self, name, parent = None):
        super().__init__(name)
        self.children = list()
        self._total_size = None
        self._child_changed = True

        if parent is not None:
            self._parent : Dir = parent

    @property
    def parent(self):
        return self._parent
    @property
    def get_size(self):
        # we already calculated, so no need to calculate again
        if not self._child_changed:
            return self._total_size

        def _get_size_for(obj: File | Dir):
            if type(obj) is File:
                return obj.total_size
            elif type(obj) is Dir:
                return obj.get_size
            # Wrong type
            else:
                raise ValueError("Wrong entity type!", obj, type(obj))

        curr_size = 0
        # we need to calculate
        for c in self.children:
            curr_size += _get_size_for(c)

        # we calculated the size, so, update the variables
        self._child_changed = False
        self._total_size = curr_size
        return curr_size

def parse_commands(file_obj):

    # first command seems to always be the root, so, create that
    CHANGE_ROOT = ChangeDir(SpecialDir.ROOT)
    file_obj.readline() # and ignore it

    commands = deque()
    commands.append(CHANGE_ROOT)

    curr_command = None
    for line in file_obj:
        # sanitize the line for line-feeds
        line = line.rstrip()
        # it's a command, so
        if line.startswith("$"):
            match line.lstrip("$ ").split(" "):
                case [CommandType.ListFiles]:
                    curr_command = ListFiles()
                case [CommandType.ChangeDir, SpecialDir.ROOT]:
                    curr_command = CHANGE_ROOT
                case [CommandType.ChangeDir, SpecialDir.PARENT]:
                    curr_command = ChangeDir(SpecialDir.PARENT)
                case [CommandType.ChangeDir, arg]:
                    curr_command = ChangeDir(arg)
                case _:
                    raise ValueError("Error in parsing")
            # after we got our command, just append that to the command list

            commands.append(curr_command)
            continue

        # it's not a command, so we're probably on an LS feed. Which means, we can just keep appending to the result
        else:
            curr_command.result.append(line)

    return commands


def day_7(file_obj):
    # just for helper
    ROOT_DIR = Dir(SpecialDir.ROOT)
    with open("sol_snake\example_7.txt") as f:
        commands = parse_commands(f)
        print(commands)

        return ROOT_DIR.get_size