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


def move_tail(
    curr_tail: Coordinate,
    curr_head: Coordinate,
    next_head: Coordinate,
    direction: Direction,
) -> Coordinate:
    # check if we're still touching the head with the tail
    is_touching, _ = tail_is_touching(curr_tail, next_head)
    if is_touching:
        # if we are, we can stay in the same position
        return curr_tail
    else:
        # if not, we need to move the tail accordingly
        # so first, check the relative position of the previous head position
        _, was_touching_dir = tail_is_touching(curr_tail, curr_head)
        # We already know we're not touching, so we're 2 steps away
        # If we were diagonally, that means we moved further, so we also need to move also diagonally
        if was_touching_dir.is_diagonal():
            return get_move(curr_tail, was_touching_dir)
        # otherwise, we can just move in the same direction
        else:
            # move tail same way
            return get_move(curr_tail, direction)


def day_9(file_obj):
    example = open("sol_snake\example_9.txt", encoding="utf-8")
    visited_coords = {}
    all_moves: list[Move] = parse_moves(file_obj)

    # Initial conditions
    START_POS = (0, 0)

    main_pos_head = START_POS
    main_pos_tail = START_POS
    visited_coords[START_POS] = 1

    for move in all_moves:
        # logic for main solution
        for i in range(move.distance):
            # Move Head
            next_head = get_move(main_pos_head, move.direction)

            # Tail Logic
            next_tail = move_tail(main_pos_tail, main_pos_head, next_head, move.direction)
            # they should be touching
            assert tail_is_touching(next_tail, next_head)

            # Update logic
            main_pos_head = next_head
            main_pos_tail = next_tail
            # register the visit
            visited_coords[main_pos_tail] = visited_coords.get(main_pos_tail, 0) + 1


    # Logic for 2nd solution
    TOTAL_SEGMENTS = 10
    

    return len(visited_coords.keys())
