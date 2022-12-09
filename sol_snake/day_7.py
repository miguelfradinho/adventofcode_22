from dataclasses import dataclass
from typing import Optional


@dataclass
class File:
    name : str
    size : int

class Dir:
    def __init__(self, name: str, parent = None):
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

def day_7(file_obj):


