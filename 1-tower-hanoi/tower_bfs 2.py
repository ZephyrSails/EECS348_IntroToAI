import copy
from collections import defaultdict

def hanoi(pegs, disks):
    state = [[] for x in range(pegs)]
    state[0] = [x for x in range(disks, 0, -1)]
    target = [[] for x in range(pegs)]
    target[-1] = [x for x in range(disks, 0, -1)]
    tried = []

    # worst_steps = 2 ** disks - 1
    # worst_steps = 5
    move_set = []
    [parent, arr] = bfs(state, target, tried, move_set, 0, 1)
    # print back_trace(parent, arr)
    print len(arr), len(parent)
    # print parent
    # print arr
    # move_set.reverse()
    return back_trace(parent, arr)

def back_trace(parent, arr):
    path = []
    current = len(arr)-1
    while current != '?':
        path.append(arr[current])
        # print current
        print current
        current = parent[current]
    path.pop()
    path.reverse()
    return path

def bfs(state, target, tried, move_set, depth, testing_depth):
    if state == target:
        return True

    # good_moves = get_moves(state)

    current_level_states = [state]
    next_level_states = []
    depth = 0

    # num_count = 0
    arr = [True]
    # k = 0
    # graph = {0: []}
    graph = defaultdict(lambda: [])
    node = -1
    parent = {0: '?'}
    # move_set = []
    while True:
        depth += 1
        level_move_count = 0
        for stt in current_level_states:
            node += 1
            good_moves = get_moves(stt)
            for good_move in good_moves:
                level_move_count += 1
                graph[node].append(len(arr))
                parent[len(arr)] = node
                arr.append(good_move)

                new_state = move(stt, good_move[0], good_move[1])
                if new_state == target:
                    return [parent, arr]
                else:
                    next_level_states.append(new_state)

                    # move_set.pop()
        current_level_states = next_level_states
        next_level_states = []


def move(state, fr, to):
    new_state = copy.deepcopy(state)
    new_state[to].append(new_state[fr].pop())
    return new_state

def get_moves(state):
    good_move = []
    for fr in range(len(state)):
        if state[fr]:
            if state[fr]:
                for to in range(len(state)):
                    if state[to]==[] or state[to] and state[to][-1] > state[fr][-1]:
                        good_move.append([fr, to])
                # else if
    return good_move

def deja_vu(tried, state):
    for st in tried:
        if state == st:
            return True
    return False

if __name__ == '__main__':
    print hanoi(6, 6)
