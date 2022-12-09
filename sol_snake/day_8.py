import numpy as np
from pprint import pprint


def array_to_file(shape: tuple[int, int], map:dict):
    visible_trees = np.zeros(shape)
    for k, v in map.items():
        if any(v):
            visible_trees[k] = 1
    np.savetxt("example_test.txt", visible_trees, fmt="%1.0f", encoding="utf-8")



def day_8(file_obj):
    example = open("sol_snake\example_8.txt")

    all_trees = []
    with file_obj as f:
        for line in f:
            line = line.strip()
            all_trees.append([int(i) for i in line])

    all_trees: np.ArrayLike = np.array(all_trees)
    # number of rows and columns are the same
    n_rows, n_cols = all_trees.shape
    # -4 since we're counting the corners 4 times 
    edge_trees = n_rows*2 + n_cols*2 - 4
    visible_map = dict()

    # we never need to check the edges, so
    inside_trees_coord = [(i, j) for i in range(1, n_rows-1) for j in range(1, n_cols-1)]

    for coord in inside_trees_coord:
        bot, top, left, right = [False]*4
        #is_visible = visible_inside.get(coord, False)
        x, y = coord
        elem = all_trees[x, y]
        # check all behind (left)
        if all(elem > all_trees[x, :y]):
            #print(coord, elem, "has all behind shorter")
            left = True

        # check all forward (right)
        if all(elem > all_trees[x, y + 1:]):
            #print(coord, elem, "has all forward shorter")
            right = True

        # check all upwards (top)
        if all(elem > all_trees[:x, y]):
            #print(coord,elem, "all upwards shorter")
            top = True

        # check all downwards (bottom)
        if all(elem > all_trees[x+1:, y]):
            #print(coord, elem, "all downwards shorter")
            bot = True

        visible_map[coord] = (left, right, top, bot)

    #array_to_file((n_rows, n_cols), visible_map)

    return edge_trees + len([k for k, v in visible_map.items() if any(v)])
