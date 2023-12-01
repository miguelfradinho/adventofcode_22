import numpy as np
from pprint import pprint


def array_to_file(shape: tuple[int, int], map: dict):
    visible_trees = np.zeros(shape)
    for k, v in map.items():
        if any(v):
            visible_trees[k] = 1
    np.savetxt("example_test.txt", visible_trees, fmt="%1.0f", encoding="utf-8")


def get_score_for_lines(elem, blocking_trees, reverse=False):
    if reverse:
        blocking_trees = reversed(blocking_trees)
    score = 0
    for i in blocking_trees:
        # always sum cuz we need to count nth tree
        score += 1
        # break if bigger tree
        if i >= elem:
            break
    return score


def day_8(file_obj):
    example = open("sol_snake\\example_8.txt")

    all_trees = []
    with file_obj as f:
        for line in f:
            line = line.strip()
            all_trees.append([int(i) for i in line])

    all_trees: np.ArrayLike = np.array(all_trees)
    # number of rows and columns are the same
    n_rows, n_cols = all_trees.shape
    # -4 since we're counting the corners 4 times
    edge_trees = n_rows * 2 + n_cols * 2 - 4
    visible_map = dict()

    # we never need to check the edges, so
    inside_trees_coord = [
        (i, j) for i in range(1, n_rows - 1) for j in range(1, n_cols - 1)
    ]

    for coord in inside_trees_coord:
        bot, top, left, right = [False] * 4

        x, y = coord
        elem = all_trees[x, y]

        elems_left = all_trees[x, :y]
        score = 1
        # check all behind (left)
        if all(elem > elems_left):
            # print(coord, elem, "has all behind shorter")
            left = True
        # we have to reverse because we're going behind
        score *= get_score_for_lines(elem, elems_left, reverse=True)

        elems_right = all_trees[x, y + 1 :]
        # check all forward (right)
        if all(elem > elems_right):
            # print(coord, elem, "has all forward shorter")
            right = True
        score *= get_score_for_lines(elem, elems_right)

        elems_up = all_trees[:x, y]
        # check all upwards (top)
        if all(elem > elems_up):
            # print(coord,elem, "all upwards shorter")
            top = True
        # we have to reverse because we're going upwards (behind)
        score *= get_score_for_lines(elem, elems_up, reverse=True)

        elems_bot = all_trees[x + 1 :, y]
        # check all downwards (bottom)
        if all(elem > elems_bot):
            # print(coord, elem, "all downwards shorter")
            bot = True
        score *= get_score_for_lines(elem, elems_bot)

        visible_map[coord] = (elem, score, left, right, top, bot)

    # array_to_file((n_rows, n_cols), visible_map)
    visible_trees = [k for k, v in visible_map.items() if any(v[2:])]
    total_visible = edge_trees + len(visible_trees)
    max_score = max([visible_map[k][1] for k in visible_trees])
    return total_visible, max_score
