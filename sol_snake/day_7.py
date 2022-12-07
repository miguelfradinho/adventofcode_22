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
def day_7(file_obj):
    return None