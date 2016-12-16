import copy
import random

def hanoi(pegs, disks):
    state = [[] for x in range(pegs)]
    state[0] = [x for x in range(disks, 0, -1)]
    target = [[] for x in range(pegs)]
    target[-1] = [x for x in range(disks, 0, -1)]
    tried = []

    worst_steps = 2 ** disks - 1
    # worst_steps = 5
    # tried.append(state)
    move_set = []
    dfs(state, target, tried, move_set, worst_steps)
    move_set.reverse()
    return move_set
    # return None

def dfs(state, target, tried, move_set, worst_steps, stack_depth=0):
    if state == target:
        return True
    if stack_depth == worst_steps or deja_vu(tried, state):
        return False
    tried.append(state)
    for good_move in get_moves(state):
        new_state = move(state, good_move[0], good_move[1])
        if dfs(new_state, target, tried, move_set, worst_steps, stack_depth+1):
            move_set.append(good_move)
            return True
    tried.pop()
    return False

# def get_moves(state):

# def compare(state1, state2):
#     return state1 == state2

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
    # random.shuffle(good_move)
    return good_move

def deja_vu(tried, state):
    for st in tried:
        if state == st:
            return True
    return False

if __name__ == '__main__':
    print hanoi(6, 6)
