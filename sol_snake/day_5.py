from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Move:
    n_crates: int
    start_stack: int
    end_stack: int

    @staticmethod
    def parse_move(move: str):
        move_data = []
        # structure is "move Nth(crates) from Start to End"
        for el in move.split(" "):
            try:
                move_data.append(int(el))
            except ValueError:
                # If it errors, we're not interested, so
                pass
        n = move_data[0]
        s = move_data[1]
        e = move_data[2]
        return Move(n_crates=n, start_stack=s, end_stack=e)


def create_stacks(lines: list[str]):

    # last line always has the columns numbered
    stacks_numbers = lines[-1].split(" " * 2)
    total_stacks = int(stacks_numbers[-1])
    stacks = [deque() for _ in range(total_stacks)]

    # each crate is enclosed in square brackets, identified with a letter and they are separated by spaces
    # [B] [C]     [e]
    # so, we can read always 4 chars by 4 chars, and we'll be able to find which crates match what

    for line in lines[:-1]:
        for i in range(0, len(line), 4):
            crate_info = line[i : i + 4]
            # ignore the space delimiters
            crate_info = crate_info.strip()
            if crate_info == "":
                # empty crate, so just skip it
                continue
            # not empty, so add it to the stack
            index = int(i / 4)  # because we're going 4 by 4
            stacks[index].appendleft(crate_info)
    return stacks


def day_5(file_obj):
    # Structure of the file is always:
    # Nth crates split across Mth collumns
    # followed by a blank line
    # followed by moves
    stacks_data = []
    moves_data = []
    current_append = stacks_data
    with file_obj as f:
        for line in f:
            line = line.strip("\n")
            # when we reach the blank line, switch which we're appending to
            if line == "":
                current_append = moves_data
                # and skip it
                continue
            current_append.append(line)

    all_moves = [Move.parse_move(i) for i in moves_data]
    stacks_9000 = create_stacks(stacks_data)
    stacks_9001 = create_stacks(stacks_data)

    for move in all_moves:
        # process for 9000
        for i in range(move.n_crates):
            crate = stacks_9000[move.start_stack - 1].pop()
            stacks_9000[move.end_stack - 1].append(crate)

        # process for 9001
        # it can move multiple, so, retain same behaviour when only moving 1 crate
        if move.n_crates == 1:
            crate = stacks_9001[move.start_stack - 1].pop()
            stacks_9001[move.end_stack - 1].append(crate)
        # otherwise we need to invert how we place them
        else:
            crates_to_add = [
                stacks_9001[move.start_stack - 1].pop() for _ in range(move.n_crates)
            ]
            for i in crates_to_add[::-1]:
                stacks_9001[move.end_stack - 1].append(i)

    answer_9000 = (
        "".join([i.pop() for i in stacks_9000]).replace("]", "").replace("[", "")
    )
    answer_9001 = (
        "".join([i.pop() for i in stacks_9001]).replace("]", "").replace("[", "")
    )
    return answer_9000, answer_9001
