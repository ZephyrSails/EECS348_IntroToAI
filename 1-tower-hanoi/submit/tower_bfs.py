import copy
from collections import defaultdict
import sys

def hanoi(pegs, disks):
    state = [[] for x in range(pegs)]
    state[0] = [x for x in range(disks, 0, -1)]
    target = [[] for x in range(pegs)]
    target[-1] = [x for x in range(disks, 0, -1)]
    tried = []

    move_set = []
    [parent, arr] = bfs(state, target, tried, move_set, 0, 1)

    return back_trace(parent, arr)

def back_trace(parent, arr):
    path = []
    current = len(arr)-1
    while current != '?':
        path.append(arr[current])
        # print current
        current = parent[current]
    path.pop()
    path.reverse()
    return path

def bfs(state, target, tried, move_set, depth, testing_depth):
    if state == target:
        return True
    current_level_states = [state]
    next_level_states = []
    depth = 0
    arr = [True]
    # Graph and parent and node is for back tracing bfs tree
    graph = defaultdict(lambda: [])
    parent = {0: '?'}
    node = -1
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
    return good_move

# Did I seen this state already?
def deja_vu(tried, state):
    for st in tried:
        if state == st:
            return True
    return False

if __name__ == '__main__':
    print hanoi(int(sys.argv[1]), int(sys.argv[2]))
