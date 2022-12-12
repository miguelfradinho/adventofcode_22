import typing
from enum import Enum
from dataclasses import dataclass


class Direction(Enum):
    Up = 1
    DiagonalRightUp = 5
    Right = 2
    DiagonalRightDown = 6
    Down = 3
    DiagonalLeftDown = 7
    Left = 4
    DiagonalLeftUp = 8

    def is_diagonal(self):
        match self:
            case Direction.DiagonalRightUp:
                return True
            case Direction.DiagonalRightDown:
                return True
            case Direction.DiagonalLeftDown:
                return True
            case Direction.DiagonalLeftUp:
                return True
        return False

    def is_cardinal(self):
        match self:
            case Direction.Up:
                return True
            case Direction.Right:
                return True
            case Direction.Down:
                return True
            case Direction.Left:
                return True
        return False

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


@dataclass
class Move:
    direction: Direction
    distance: int


Coordinate = tuple[int, int]


def parse_moves(file_obj) -> list[Move]:
    all_moves: list[Move] = []
    with file_obj as f:
        for line in f:
            line = line.strip()
            direction, amount = line.split(" ")
            m = Move(Direction.from_string(direction), int(amount))
            all_moves.append(m)
    return all_moves


# We only need to check, regardless of the direction
def tail_is_touching(
    tail: Coordinate, head: Coordinate
) -> tuple[bool, typing.Optional[Direction]]:
    # Overlapping
    if tail == head:
        return True, None

    # check in all directions
    for d in Direction:
        if get_move(tail, d) == head:
            return True, d

    return False, None


def get_move(coord: Coordinate, direction: Direction) -> Coordinate:
    x, y = coord

    match direction:
        case Direction.Up:
            return x, y + 1

        case Direction.DiagonalRightUp:
            return x + 1, y + 1

        case Direction.Right:
            return x + 1, y

        case Direction.DiagonalRightDown:
            return x + 1, y - 1

        case Direction.Down:
            return x, y - 1

        case Direction.DiagonalLeftDown:
            return x - 1, y - 1

        case Direction.Left:
            return x - 1, y

        case Direction.DiagonalLeftUp:
            return x - 1, y + 1

        case other:
            raise ValueError("Wrong parsing", other)


def day_9(file_obj):
    example = open("sol_snake\example_9.txt", encoding="utf-8")
    visited_coords = {}
    all_moves: list[Move] = parse_moves(file_obj)

    # Initial conditions
    START_POS = (0, 0)
    pos_head = START_POS
    pos_tail = pos_head
    visited_coords[pos_tail] = 1

    for move in all_moves:
        for i in range(move.distance):
            # get the next position
            next_head = get_move(pos_head, move.direction)
            # check if we're still touching the head with the tail
            is_touching, _ = tail_is_touching(pos_tail, next_head)
            if is_touching:
                # if we are, we can stay in the same position
                next_tail = pos_tail
            else:
                # if not, we need to move the tail accordingly
                # so first, check the relative position of the previous head position
                _, was_touching_dir = tail_is_touching(pos_tail, pos_head)
                # We already know we're not touching, so we're 2 steps away
                # If we were diagonally, that means we moved further, so we also need to move also diagonally
                if was_touching_dir.is_diagonal():
                    next_tail = get_move(pos_tail, was_touching_dir)
                # otherwise, we can just move in the same direction
                else:
                    # move tail same way
                    next_tail = get_move(pos_tail, move.direction)

                # they should be touching
                assert tail_is_touching(next_tail, next_head)
            # update the position of both
            pos_head = next_head
            pos_tail = next_tail
            # register the visit
            visited_coords[pos_tail] = visited_coords.get(pos_tail, 0) + 1
            print("head", pos_head, "tail:", pos_tail)

    return len(visited_coords.keys())
