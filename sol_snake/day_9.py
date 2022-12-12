from enum import Enum
from dataclasses import dataclass
from typing import Optional


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
def tail_is_touching(tail: Coordinate, head: Coordinate) -> bool:
    # Overlapping
    if tail == head:
        return True

    # Use man
    # check in all directions
    for d in Direction:
        if get_move(tail, d) == head:
            return True

    return False


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


def get_relative_direction(tail: Coordinate, head: Coordinate) -> Optional[Direction]:
    # Check if they're touching, if they're, don't move
    if tail_is_touching(tail, head):
        return None

    tail_x, tail_y = tail
    head_x, head_y = head
    # we're on same Horizontal axis, so it's either up or down
    if tail_x == head_x:
        return Direction.Up if tail_y < head_y else Direction.Down
    # we're on same Vertical axis, so either right or left
    elif tail_y == head_y:
        return Direction.Right if tail_x < head_x else Direction.Left
    # not on either axis, so we have to go diagonally
    else:
        # we're behind, so it's either RightUp or RightDown
        if tail_x < head_x:
            # if we're below it, RightUp, otherwise we're above it, so
            return (
                Direction.DiagonalRightUp
                if tail_y < head_y
                else Direction.DiagonalRightDown
            )
        # we're ahead, so it's either LeftUp or LeftDown
        else:
            # if we're below it, LeftUp, otherwise we're above it, so
            return (
                Direction.DiagonalLeftUp
                if tail_y < head_y
                else Direction.DiagonalLeftDown
            )


def solve_rope_motion(
    moves: list[Move], start_pos: Coordinate = (0, 0), tail_segments: int = 1
) -> dict[Coordinate, int]:
    visited: dict[Coordinate, int] = {}
    # initial conditions
    curr_head = start_pos
    segments = [start_pos for _ in range(tail_segments)]
    for move in moves:
        for _ in range(move.distance):
            # Move Head
            next_head = get_move(curr_head, move.direction)
            # Tail Logic
            head_to_follow = next_head
            # Move each segment
            for i in range(tail_segments):
                curr_tail = segments[i]
                dir_to_move = get_relative_direction(curr_tail, head_to_follow)
                # only move if we're not touching or overlapping
                if dir_to_move is not None:
                    next_tail = get_move(curr_tail, dir_to_move)
                else:
                    next_tail = curr_tail
                # update the segment position
                segments[i] = next_tail
                head_to_follow = next_tail

            # Update logic
            curr_head = next_head
            # register the visit of only the last one
            visited[segments[-1]] = visited.get(segments[-1], 0) + 1
    return visited


def day_9(file_obj):
    example = open("sol_snake\\example_9.txt", encoding="utf-8")

    all_moves: list[Move] = parse_moves(file_obj)
    main_visited = solve_rope_motion(all_moves)
    bonus_visited = solve_rope_motion(all_moves, tail_segments=9)

    return len(main_visited.keys()), len(bonus_visited.keys())
