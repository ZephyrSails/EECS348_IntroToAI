# Zhiping X. 2016-09-29 20:36:36 -0500
import copy
import sys
# USAGE: python tower.py <pegs> <disks>


def hanoi(pegs, disks):
    state_space = get_n_d_boolean_space(disks, pegs)
    # 0 : un searched
    # -1: searched
    # 1 : target
    # mark target
    set_value_from_n_d_space(state_space, [pegs-1 for i in range(disks)], 1)
    # mark starting point
    set_value_from_n_d_space(state_space, [0 for i in range(disks)], -1)

    return bfs(state_space, [0 for i in range(disks)], pegs)


def bfs(space, start_coord, pegs):
    queue = [(start_coord, [start_coord])]
    while queue:
        (coord, path) = queue.pop(0)
        for next in get_valid_moves(space, coord, pegs):
            # get_value_from_n_d_space(space, next)
            if get_value_from_n_d_space(space, next) == 1:
                return path + [next]
            else:
                set_value_from_n_d_space(space, next, -1)
                queue.append((next, path + [next]))


def get_valid_moves(space, state, pegs):
    ans = []
    for i in range(len(state)):
        # smaller disks' position: state[:i]
        # current disk's position: state[i]
        # bigger disks' position: state[i+1:]
        covered = False
        # can only move to bigger disk
        smaller_standing_points = set([state[i]])
        for smaller_disk_position in state[:i]:
            # if covered by smaller disk, can't move
            if smaller_disk_position == state[i]:
                covered = True
                break
            else:
                smaller_standing_points.add(smaller_disk_position)
        if not covered:
            for valid_peg in list((set([k for k in range(pegs)]) - smaller_standing_points)):
                valid_coord = copy.copy(state)
                valid_coord[i] = valid_peg
                # move = [i, valid_peg]
                if get_value_from_n_d_space(space, valid_coord) >= 0:
                    # ans.append((move, valid_coord))
                    ans.append(valid_coord)
    return ans


def get_n_d_boolean_space(n, m):
    if n == 1:
        return [0 for i in range(m)]
    return [get_n_d_boolean_space(n-1, m) for i in range(m)]


def get_value_from_n_d_space(space, coordinate):
    if len(coordinate) == 1:
        return space[coordinate[0]]
    return get_value_from_n_d_space(space[coordinate[0]], coordinate[1:])


def set_value_from_n_d_space(space, coordinate, value):
    if len(coordinate) == 1:
        space[coordinate[0]] = value
        return
    return set_value_from_n_d_space(space[coordinate[0]], coordinate[1:], value)

if __name__ == '__main__':
    print hanoi(int(sys.argv[1]), int(sys.argv[2]))
