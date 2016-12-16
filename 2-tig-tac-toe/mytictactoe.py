#   X: -1
#   O: 1
#   0: None
def mymove(board,mysymbol):
    print "Board as seen by the machine:",
    print board
    print "The machine is playing:",
    print mysymbol

    moving_piece = 1 if mysymbol == 'X' else -1
    return negamax(board, -5, 5, moving_piece)[1] + 1
    # return int(raw_input("Machine? "))


#   Instead of using minmax, we use negamax method.
#   Which is a variants of minmax, based on same logic.
#   But it requires less code and easier to re-use.
def negamax(board, alpha, beta, moving_piece, depth=0):
    board_score, end_flag = eva(board)
    # print board_score, board
    if end_flag:
        return moving_piece * board_score
    best_score = -5
    best_move = None
    if depth == 1:
        win_count = 0
        total_count = 0
    for i in xrange(len(board)):
        if board[i] == 0:
            next_board = board[:]
            next_board[i] = moving_piece
            score = -negamax(next_board, -beta, -alpha, -moving_piece, depth+1)
            if depth == 1:
                win_count += score
                total_count += 1
            if score > best_score:
                best_score = score
                best_move = i
            # best_score = max([best_score, score])
            alpha = max([alpha, score])
            if depth == 0:
                print score, next_board, alpha, beta
            if alpha >= beta and depth != 1:
                break
    if depth == 1:
        return float(win_count) / total_count if best_score == 0 else best_score
    if depth == 0:
        return best_score, best_move
    else:
        return best_score
    if depth == 0:
        return float(win_count) / total_count if best_score == 0 else best_score, best_move
    else:
        return float(win_count) / total_count if best_score == 0 else best_score


#   Evaluate the board, score it.
#   -1, true    : O win, game end
#   1,  true    : X win
#   0,  true    : tie, game end
#   0,  false   : not sure, game continues
def eva(board):
    # see if someone win:
    for i in xrange(3): # Check columns and rows:
        if board[i] == board[3+i] == board[6+i]:
            if not board[i] == 0:
                return board[i], True
        if board[i*3] == board[i*3+1] == board[i*3+2]:
            if not board[i*3] == 0:
                return board[i*3], True
    # Check X:
    if board[0] == board[4] == board[8] or board[2] == board[4] == board[6]:
        if not board[4] == 0:
            return board[4], True
    # No one wins:
    if 0 in board:
        return 0, False # board not full
    else:
        return 0, True  # board full


#   Test cases
def test_negemax():
    print negamax([0,0,0,0,0,0,0,0,0], -5, 5, 1) == 0
    print negamax([0,0,-1,0,1,0,0,0,0], -5, 5, 1) == 0
    print negamax([-1,0,-1,0,1,0,0,0,1], -5, 5, 1) == 0
    print negamax([-1,1,-1,0,1,0,0,-1,1], -5, 5, 1) == 0
    print negamax([-1,1,-1,0,1,0,0,-1,1], -5, 5, 1) == 0
    print negamax([-1,1,-1,1,1,-1,0,-1,1], -5, 5, 1) == 0
    print negamax([-1,1,-1,1,1,-1,1,-1,1], -5, 5, 1) == 0
    print negamax([1, 1, -1, 1, -1, 0, 0, 0, 0], -5, 5, 1) == 0
    print negamax([1, 1, -1, 0, -1, 0, 0, 0, 0], -5, 5, 1) == 0
    print negamax([0, -1, 0, 0, 0, 0, 0, 0, 0], -5, 5, 1)


#   Testing all wining cases
def test_eva():
    print eva([1,1,1,0,0,0,0,0,0])
    print eva([0,0,0,1,1,1,0,0,0])
    print eva([0,0,0,0,0,0,1,1,1])
    print eva([1,0,0,1,0,0,1,0,0])
    print eva([0,1,0,0,1,0,0,1,0])
    print eva([0,0,1,0,0,1,0,0,1])
    print eva([1,0,0,0,1,0,0,0,1])
    print eva([0,0,1,0,1,0,1,0,0])
