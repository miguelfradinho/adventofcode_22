from .data_types import Coordinate
elevation_chars = "abcdefghijklmnopqrstuvwxyz"

StartPos = "S"
EndPos = "E"

def get_score(elevation):
    # starting position
    if elevation == StartPos:
        return -1
    if elevation == EndPos:
        return 999
    if elevation in elevation_chars:
        return elevation_chars.index(elevation)+1


def parse_input(file_obj) -> tuple[tuple[Coordinate, Coordinate], dict[Coordinate, int]]:

    start_pos = None
    end_pos = None
    row_index = 0
    score_map:  dict[Coordinate, int] = {}

    with file_obj as f:
        for line in f:
            line = line.strip()
            for j in range(len(line)):
                curr_char = line[j]
                # Temp variable so we're not always typing it
                curr_coords : Coordinate = (row_index, j)
                # Check if we already found the special chars, and store them
                if start_pos is None and curr_char == StartPos:
                    start_pos = curr_coords
                elif end_pos is None and curr_char == EndPos:
                    end_pos = curr_coords

                # Get the current score
                curr_score = get_score(curr_char)
                # and store it in the map
                score_map[curr_coords] = curr_score
            # a new line = a new row, so, increase the counter
            row_index += 1

    return (start_pos, end_pos), score_map


def day_12(file_obj):
    example = open("sol_snake\example_12.txt", encoding="utf-8")
    positions, score_map = parse_input(example)
    return positions, score_map