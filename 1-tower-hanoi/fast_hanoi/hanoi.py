# Zhiping X. 2016-09-29 20:36:36 -0500
import copy
import sys
# USAGE: python tower.py <disks> <pegs>

# Used a special method to model n disks, m pegs hanoi problem,
# Oct 1:
# Soving 7 disks, 7 pegs hanoi problem with optimal answer in 30 secs, in 8 GB 2.7 GHz i5 macbook.
# Sept 29:
# Soving 7 disks, 7 pegs hanoi problem with optimal answer in 3 mins, in 8 GB 2.7 GHz i5 macbook.
# Came up with this idea in EECS 325 Intro to AI courses.

# The searching method is normal, bfs, but the modeling method might be helpful later.
# If you want to use my idea, please cite this page, thank you~


def hanoi(pegs, disks):
    # n dimension state space. And actually is not boolean space.
    state_space = get_n_d_boolean_space(disks, pegs)
    # 0 : un searched
    # -1: searched
    # 1 : target
    # mark target
    set_value_from_n_d_space(state_space, [pegs-1 for i in range(disks)], 1)
    # mark starting point
    set_value_from_n_d_space(state_space, [0 for i in range(disks)], -1)

    return bfs(state_space, [0 for i in range(disks)], pegs)


# This cool bfs path_backtrace method was learned from
# http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
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
                # move = [state[i], valid_peg]
                if get_value_from_n_d_space(space, valid_coord) >= 0: # Deja vu?
                    # One dim faster:
                    if i != len(state)-1 or valid_peg == pegs-1:
                        ans.append(valid_coord)
                    # ans.append((move, valid_coord))
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

# hanoi(3, 3)
