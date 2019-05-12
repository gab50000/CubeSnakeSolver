#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import product
import numpy as np
import ipdb

start_cfg = "ddrddrdrrrdrrdrrdrrdrdrdrdrddrrdrdrdrrdddrdrdddrddrdrdrdrdrdddr"
COUNTER = 0


def count_hinges(cfg):
    hinge_counter = 0
    x = cfg[0]

    for d in cfg:
        if x != d:
            hinge_counter += 1
            x = d
    return hinge_counter


TOTAL_CONFIGS = 4 ** count_hinges(start_cfg)


def userfriendly_output(numpy_direction):
    if (numpy_direction == [1, 0, 0]).all():
        return "x"
    elif (numpy_direction == [-1, 0, 0]).all():
        return "-x"
    elif (numpy_direction == [0, 1, 0]).all():
        return "y"
    elif (numpy_direction == [0, -1, 0]).all():
        return "-y"
    elif (numpy_direction == [0, 0, 1]).all():
        return "z"
    elif (numpy_direction == [0, 0, -1]).all():
        return "-z"
    else:
        raise ValueError("Not sure what to do with this input...")


def make_matrix(cfg):
    matrix = np.zeros((64, 64), int)
    matrix[0, 0] = 1

    i, j = 0, 0

    for direction in start_cfg:
        if direction == "l":
            i += 1
        elif direction == "r":
            j += 1

        matrix[i, j] = 1

    return matrix


def still_solvable(cube, start_point):
    # check if there is a part of the cube that still needs to be filled, but cannot be reached anymore
    # at the moment: check if there is a completely filled slice of the cube, which is between the current endpoint of the snake and an empty cube part
    # better: check if there is no possible path from the endpoint to the empty part, but probably also more expensive...
    for i in range(1, cube.shape[0] - 1):
        if cube[i, :, :].all():
            if start_point[0] > i:
                for j in range(1, i):
                    if not cube[j, :, :].all():
                        return False
            elif start_point[0] < i:
                for j in range(i, cube.shape[0] - 1):
                    if not cube[j, :, :].all():
                        return False
        elif cube[:, i, :].all():
            if start_point[1] > i:
                for j in range(1, i):
                    if not cube[:, j, :].all():
                        return False
            elif start_point[1] < i:
                for j in range(i, cube.shape[0] - 1):
                    if not cube[:, j, :].all():
                        return False
        elif cube[:, :, i].all():
            if start_point[2] > i:
                for j in range(1, i):
                    if not cube[:, :, j].all():
                        return False
            elif start_point[2] < i:
                for j in range(i, cube.shape[0] - 1):
                    if not cube[:, :, j].all():
                        return False
    return True


def continue_cube(cube, start_point, directionlist, cfg, moves_remaining) -> bool:
    global COUNTER
    # find out length of new segment:
    direction = directionlist[-1]
    length = 0

    if len(cfg) == 0:
        COUNTER += 1
        return False
    x = cfg[0]
    while cfg[0] == x:
        length += 1
        cfg = cfg[1:]
        if len(cfg) == 0:
            break

    if still_solvable(cube, start_point):
        for i in range(1, length + 1):
            # ~ ipdb.set_trace()
            new_point = start_point + i * direction
            if (new_point > 3).any() or (new_point < 0).any():
                # ~ print "not possible"
                # ~ print directionlist
                COUNTER += 4 ** (moves_remaining - 1)
                return False
            else:
                # ~ ipdb.set_trace()
                if cube[new_point[0], new_point[1], new_point[2]] == 0:
                    cube[new_point[0], new_point[1], new_point[2]] = 1
                else:
                    # ~ print "not possible"
                    # ~ print directionlist
                    COUNTER += 4 ** (moves_remaining - 1)
                    return False

            if COUNTER % 100 == 0:
                print(
                    f"Sum {cube.sum():2d}, progress: {COUNTER/TOTAL_CONFIGS:.4%}",
                    end="\r",
                )
        if (cube == 1).all():
            print("Found solution")
            for d in directionlist:
                print(d)
            return True
    else:
        # ~ print "not solvable anymore"
        COUNTER += 4 ** moves_remaining
        return False

    new_startpoint = start_point + length * direction

    newdirs = np.where(direction == 0)[0]

    for newdir in newdirs:
        for i in [-1, 1]:
            newlist = list(directionlist)
            newcube = np.copy(cube)
            arr = np.zeros(3, int)
            arr[newdir] = i
            newlist.append(arr)
            if (
                continue_cube(
                    newcube, new_startpoint, newlist, cfg, moves_remaining - 1
                )
                == True
            ):
                return True
    return False
    # ~ dirs.append(arr)


def make_cube(cfg):
    directionlist = []
    directionlist.append(np.array([1, 0, 0]))

    hinge_nr = count_hinges(cfg)
    # find startconfig
    for x, y, z in product(range(4), range(4), range(4)):
        if x + 2 < 4:
            cube = np.zeros((4, 4, 4), int)
            startpoint = np.array((x, y, z), int)
            print("startpoint", startpoint)

            for i in range(3):
                cube[startpoint[0] + i, startpoint[1], startpoint[2]] = 1
            direction = directionlist[-1]
            new_startpoint = startpoint + (2, 0, 0)
            cfg = cfg[2:]

            newdirs = np.where(direction == 0)[0]

            for newdir in newdirs:
                for i in [-1, 1]:
                    newlist = list(directionlist)
                    arr = np.zeros(3, int)
                    arr[newdir] = i
                    newlist.append(arr)
                    newcube = np.copy(cube)
                    print("testing", arr)
                    if continue_cube(
                        newcube, new_startpoint, newlist, cfg, moves_remaining=hinge_nr
                    ):
                        print("startpoint for solution", startpoint)
                        break


def main(*args):
    hinge_nr = count_hinges(start_cfg)
    print("number of hinges: {}".format(hinge_nr))
    print("possible configurations: {}".format(4 ** hinge_nr))
    make_cube(start_cfg)


if __name__ == "__main__":
    main()
