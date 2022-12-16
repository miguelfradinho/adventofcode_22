from enum import Enum
Coordinate = tuple[int, int]
class Direction(Enum):
    Up = 1
    DiagonalRightUp = 5
    Right = 2
    DiagonalRightDown = 6
    Down = 3
    DiagonalLeftDown = 7
    Left = 4
    DiagonalLeftUp = 8

    @staticmethod
    def from_string(string):
        match string:
            case "R":
                return Direction.Right
            case "L":
                return Direction.Left
            case "D":
                return Direction.Down
            case "U":
                return Direction.Up
            case _:
                raise NotImplementedError(
                    "expected one of the 4 cardinal directions, got: ", string
                )

