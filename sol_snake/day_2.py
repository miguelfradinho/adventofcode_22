import enum


class Move_them(enum.StrEnum):
    ROCK = "A"
    PAPER = "B"
    SCISSORS = "C"


class Move_me(enum.StrEnum):
    ROCK = "X"
    PAPER = "Y"
    SCISSORS = "Z"


class Move_Result(enum.StrEnum):
    # Points for the outcome
    LOSS = "X"
    DRAW = "Y"
    WIN = "Z"


class Shape(enum.IntEnum):
    # Points for the shape
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def __invert__(self) -> int:
        if self is Shape.ROCK:
            return Shape.PAPER
        if self is Shape.PAPER:
            return Shape.SCISSORS
        if self is Shape.SCISSORS:
            return Shape.ROCK

    def __xor__(self, __n: int) -> int:
        if self is Shape.ROCK:
            return Shape.SCISSORS
        if self is Shape.PAPER:
            return Shape.ROCK
        if self is Shape.SCISSORS:
            return Shape.PAPER


class Outcome(enum.IntEnum):
    # Points for the outcome
    LOSS = 0
    DRAW = 3
    WIN = 6


def get_move(move, move_map: Move_them | Move_me) -> Shape:
    match move:
        case move_map.ROCK:
            return Shape.ROCK
        case move_map.PAPER:
            return Shape.PAPER
        case move_map.SCISSORS:
            return Shape.SCISSORS
        case _:
            raise ValueError("Invalid argument", move, move_map)


def get_result(move, move_map: Move_Result) -> Shape:
    match move:
        case move_map.LOSS:
            return Outcome.LOSS
        case move_map.DRAW:
            return Outcome.DRAW
        case move_map.WIN:
            return Outcome.WIN
        case _:
            raise ValueError("Invalid argument", move, move_map)


def get_outcome_as_win(them: Shape, me: Shape) -> Outcome:
    if them == me:
        return Outcome.DRAW
    if them is Shape.ROCK:
        if me is Shape.PAPER:
            return Outcome.WIN
        return Outcome.LOSS

    if them is Shape.PAPER:
        if me is Shape.SCISSORS:
            return Outcome.WIN
        return Outcome.LOSS

    if them is Shape.SCISSORS:
        if me is Shape.ROCK:
            return Outcome.WIN
        return Outcome.LOSS


def get_outcome_as_result(them: Shape, result: Outcome) -> Shape:
    if result is Outcome.DRAW:
        return them

    elif result is Outcome.WIN:
        return ~them

    elif result is Outcome.LOSS:
        return them ^ 0

    else:
        raise ValueError(them, result)


def day_2(file_obj):
    results_as_win = []
    results_as_outcome = []
    with file_obj as f:
        for line in f:
            clean_line = line.strip()
            col1, col2 = clean_line.split(" ")

            theirs = get_move(col1, Move_them)

            # Moves as col2 = Move to win
            mine = get_move(col2, Move_me)
            results_as_win.append(mine + get_outcome_as_win(theirs, mine))

            # Moves as col2 = end result
            res = get_result(col2, Move_Result)
            results_as_outcome.append(res + get_outcome_as_result(theirs, res))

        assert len(results_as_win) == len(results_as_outcome)

        return sum(results_as_win), sum(results_as_outcome)
