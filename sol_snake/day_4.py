from typing import Tuple


def split_section(section):
    start, end = section.split("-")
    # need the extra +1 because range is exclusive
    return int(start), int(end)+1
def pair_into_range_set(pair):
    first, second = pair

    return set([i for i in range(*split_section(first))]), set([i for i in range(*split_section(second))])

def day_4(file_obj):
    with file_obj as f:
        all_pairs = [line.strip().split(",") for line in f]

    assignments = [pair_into_range_set(i) for i in all_pairs]

    count = 0
    for a in assignments:
        a : Tuple[set, set]
        f, s = a

        if s.issubset(f) or f.issubset(s):
            count +=1


    return count, len (assignments)