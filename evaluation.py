"""
Evaluation class will make more sophisticated bots
and determine the evaluation of a position
"""

from game_mod import GameState
from move_mod import Move
# from move_mod import Move
import random

CENTER_PAWNS = .3
ROOK_7TH = .3
CASTLED = .2
ROOK_ON_START_ROW = .07
NICE_KNIGHT = .25
PAWN_7TH = .35
BISHOP_OFF_START = .15
DOUBLED_PAWNS = .05
OPEN_FILE = .1


def get_material_imbalance(game: GameState):
    """
    Returns white material - black material on the board
    """
    material = 0
    for r in game.board:
        for square in r:
            piece = square[1]
            if square[0] == "w":
                if piece == "P":
                    material += 1
                if piece == "N" or piece == "B":
                    material += 3
                if piece == "R":
                    material += 5
                if piece == "Q":
                    material += 9
            elif square[0] == "b":
                if piece == "P":
                    material -= 1
                if piece == "N" or piece == "B":
                    material -= 3
                if piece == "R":
                    material -= 5
                if piece == "Q":
                    material -= 9
    return material


def end_game_eval(game: GameState):
    """
    If there are no legal moves to be made, returns either
    -inf, inf, or 0. If there are legal moves to be made, returns None
    """
    moves = game.get_legal_moves()
    eval = None
    if len(moves) == 0:
        if game.white_to_move:
            game.white_to_move = False
            blacks_next_moves = game.get_legal_moves()
            # checks if the king can be taken next move
            for move in blacks_next_moves:
                if move.piece_captured[1] == "K":
                    game.white_to_move = True
                    eval = float('-inf')
                    break
            if not game.white_to_move:
                game.white_to_move = True
                eval = 0
        else:
            game.white_to_move = True
            whites_next_moves = game.get_legal_moves()
            for move in whites_next_moves:
                if move.piece_captured[1] == "K":
                    game.white_to_move = False
                    eval = float('inf')
                    break
            if game.white_to_move:
                game.white_to_move = False
                eval = 0
    return eval


def get_evaluation(game):
    position = 0
    w_material = 0
    b_material = 0
    center_4_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    ring_1 = [(2, 2), (2, 3), (2, 4), (2, 5),
              (3, 5), (4, 5), (5, 5),
              (5, 4), (5, 3), (5, 2),
              (4, 2), (3, 2)]

    if game.white_is_castled:
        position += CASTLED
    if game.black_is_castled:
        position -= CASTLED

    for r in range(8):
        for c in range(8):
            square = game.board[r][c]
            piece = square[1]
            if square[0] == "w":
                if piece == "P":
                    w_material += 1
                    # doubled pawns
                    if game.board[r - 1][c] == "wP":
                        position -= DOUBLED_PAWNS
                    if (r, c) in center_4_squares:
                        # center pawns
                        position += CENTER_PAWNS
                    elif (r == 1):  # 7th rank
                        position += PAWN_7TH
                if piece == "N":
                    w_material += 3
                    if (r, c) in ring_1:
                        position += NICE_KNIGHT
                if (piece == "B"):
                    w_material += 3
                    if r != 7 and r != 0 and c != 0 and c != 7:
                        position += BISHOP_OFF_START
                if (piece == "R"):
                    w_material += 5
                    if r == 7:
                        position += ROOK_ON_START_ROW

                        is_open_file = True
                        for i in range(1, 8):
                            if game.board[r-i][c][0] == 'w':
                                is_open_file = False
                                break
                            elif game.board[r-i][c][0] == "b":
                                break
                        if is_open_file:
                            position += OPEN_FILE

                    elif r == 1:
                        position += ROOK_7TH
                if (piece == "Q"):
                    w_material += 9
            elif (square[0] == "b"):
                if (piece == "P"):
                    b_material += 1
                    if (game.board[r+1][c] == "bP"):
                        position -= DOUBLED_PAWNS
                    if (r, c) in center_4_squares:
                        # center pawns
                        position -= CENTER_PAWNS
                    elif (r == 6):  # 2nd rank
                        position -= PAWN_7TH
                if (piece == "N"):
                    b_material += 3
                    if (r, c) in ring_1:
                        position -= NICE_KNIGHT
                if (piece == "B"):
                    b_material += 3
                    if r != 7 and r != 0 and c != 0 and c != 7:
                        position -= BISHOP_OFF_START
                if (piece == "R"):
                    b_material += 5
                    if r == 0:
                        position -= ROOK_ON_START_ROW
                        is_open_file = True
                        for i in range(1, 8):
                            if game.board[r+i][c][0] == 'b':
                                is_open_file = False
                                break
                            elif game.board[r+i][c][0] == "w":
                                break
                        if is_open_file:
                            position -= OPEN_FILE

                    elif r == 6:
                        position -= ROOK_7TH
                if (piece == "Q"):
                    b_material += 9
    net_material = w_material - b_material
    total_material = w_material + b_material
    position = round(position, 4)
    # total starting material is 78
    if (total_material >= 10):
        evaluation = net_material + position
    else:
        end_game = end_game_eval(game)
        if end_game is None:
            evaluation = net_material
        else:
            evaluation = end_game
        evaluation = net_material
    return evaluation


def random_bot(game):
    legal_moves = game.get_legal_moves()
    return random.choice(legal_moves)


def min_legal_moves_bot(game):
    """
    returns the move that will give the opponent
    the minimum number of legal moves
    on the next turn
    """
    my_legal_moves = game.get_legal_moves()
    other_moves = {}  # keys = num moves, values = moves
    for move in my_legal_moves:
        game.make_move(move)
        their_next_moves = game.get_legal_moves()
        game.undo_move()

        num_leg = len(their_next_moves)
        if (num_leg in other_moves):
            other_moves[num_leg].append(move)
        else:
            other_moves[num_leg] = [move]
    the_min = min(other_moves.keys())
    return other_moves[the_min][0]


def min_net_legal_moves_bot(game):
    """
    returns the move that will give the opponent
    the minimum number of legal moves
    on the next turn
    """
    # assumes it is black but works regardless
    black_legal_moves = game.get_legal_moves()
    other_moves = {}  # keys = num moves, values = moves
    for move in black_legal_moves:
        game.make_move(move)
        white_next_moves = game.get_legal_moves()
        # game.undo_move()

        # find mate in 1
        num_white_legal = len(white_next_moves)
        if (num_white_legal == 0):
            return move

        black_sum = 0
        for white_move in white_next_moves:
            game.make_move(white_move)
            black_next_moves = game.get_legal_moves()
            game.undo_move()

            black_sum += len(black_next_moves)
        avg_black_moves = black_sum / (num_white_legal + 1)
        game.undo_move()
        diff = avg_black_moves * random.uniform(0, 1) - 20 * num_white_legal
        # print(avg_black_moves, num_white_legal, diff)

        if (diff in other_moves):
            other_moves[diff].append(move)
        else:
            other_moves[diff] = [move]
    the_min = min(other_moves.keys())
    return other_moves[the_min][0]


def avoid_blunder_bot(game):
    """
    returns the move that will give the opponent
    the minimum number of legal moves
    on the next turn
    """
    positions_considered = 0
    my_legal_moves = game.get_legal_moves()
    possible_moves = {}  # keys = num moves, values = moves
    for move in my_legal_moves:
        game.make_move(move)
        their_next_moves = game.get_legal_moves()
        game.undo_move()

        # find mate in 1
        num_white_legal = len(their_next_moves)
        if (num_white_legal == 0):
            return move

        good = True
        for their_move in their_next_moves:
            # don't blunder queen or m1
            if ((their_move.piece_captured[1] == "Q") or
               (len(game.get_legal_moves()) == 0)):
                good = False
            positions_considered += len(game.get_legal_moves())
        if (good):
            if (num_white_legal in possible_moves):
                possible_moves[num_white_legal].append(move)
            else:
                possible_moves[num_white_legal] = [move]
    print("Positions considered avoid blunder bot:", positions_considered)
    if (len(possible_moves) == 0):
        return my_legal_moves[0]
    else:
        the_min = min(possible_moves.keys())
        return possible_moves[the_min][0]


def material_bot(game):
    positions_considered = 0
    my_legal_moves = game.get_legal_moves()
    if (game.white_to_move):
        my_color = "w"
    else:
        my_color = "b"
    eval_move_dict = {}

    for move in my_legal_moves:
        game.make_move(move)
        next_moves = game.get_legal_moves()

        # mate in 1
        if (len(next_moves) == 0):
            game.undo_move()
            return move

        their_move_dict = {}
        for their_move in next_moves:
            game.make_move(their_move)
            my_next_legal_moves = game.get_legal_moves()
            if (len(my_next_legal_moves) == 0):
                if (my_color == "w"):
                    eval = float('-inf')
                else:
                    eval = float('inf')
            else:
                eval = get_material_imbalance(game)
            positions_considered += len(my_next_legal_moves)
            game.undo_move()

            if eval in their_move_dict:
                their_move_dict[eval].append(move)
            else:
                their_move_dict[eval] = [move]
        # find the worst case
        game.undo_move()
        if (my_color == "w"):
            worst_case_eval = min(their_move_dict.keys())
        else:
            worst_case_eval = max(their_move_dict.keys())

        if (worst_case_eval in eval_move_dict):
            eval_move_dict[worst_case_eval].append(move)
        else:
            eval_move_dict[worst_case_eval] = [move]

    # find the best worst case
    if (my_color == "w"):
        best_worst_case_eval = max(eval_move_dict.keys())
    else:
        best_worst_case_eval = min(eval_move_dict.keys())

    # print what it is considering
    # for eval in eval_move_dict:
    #     print("Eval:", eval)
    #     for m in eval_move_dict[eval]:
    #         print(m.notation)

    print("Positions considered evaluation bot:", positions_considered)
    return random.choice(eval_move_dict[best_worst_case_eval])


def value(piece_str: str):
    """
    takes in the 2nd character of a board position
    """
    if piece_str == "P":
        return 1
    elif (piece_str == "B" or piece_str == "N"):
        return 3
    elif piece_str == "R":
        return 5
    elif piece_str == "Q":
        return 9
    elif piece_str == "K":
        return float('inf')
    else:
        print("PIECE INVALID ERROR")
        return "PIECE INVALID ERROR"


def order_moves(moves: list[Move]):
    """
    Accepts a list of legal moves and orders them based on some
    preliminary good checks.
    Does not matter the color
    """
    guess_dict = {}
    for move in moves:
        if (move not in guess_dict):
            guess_dict[move] = 0
        if (move.is_check):
            guess_dict[move] += 1000
        if (move.piece_captured != '--'):
            if (value(move.piece_moved[1]) < value(move.piece_captured[1])):
                guess_dict[move] += (10 * (value(move.piece_captured[1]) -
                                           value(move.piece_moved[1])))
        if (move.promotion):
            guess_dict[move] += 70
        if (move.is_castle):
            guess_dict[move] += 100

    sorted_keys = sorted(guess_dict, key=guess_dict.get, reverse=True)
    ordered_list = list(sorted_keys)
    if len(ordered_list) != len(moves):
        print("Wrong length")

    return ordered_list


def minimax(game, depth, alpha, beta):
    """
    depth is the current depth of the search
    returns the evaluation of the best possible move for
    current player
    """
    if depth == 0:
        return get_evaluation(game)

    leg_moves = game.get_legal_moves()
    # ordered_moves = order_moves(leg_moves)
    ordered_moves = leg_moves

    if (game.white_to_move):
        if len(leg_moves) == 0:
            return float('-inf')
        # doesn't know stalemate

        max_eval = float('-inf')
        # order the moves
        for move in ordered_moves:
            game.make_move(move)
            eval = minimax(game, depth - 1, alpha, beta)
            game.undo_move()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        if len(leg_moves) == 0:
            return float('inf')
        min_eval = float('inf')

        for move in ordered_moves:
            game.make_move(move)
            eval = minimax(game, depth - 1, alpha, beta)
            game.undo_move()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def deep_bot(game, depth):
    best_move = None
    if game.white_to_move:
        best_eval = float('-inf')
    else:
        best_eval = float('inf')

    eval_move_dict = {}

    for move in game.get_legal_moves():
        game.make_move(move)
        eval = minimax(game, depth - 1, float('-inf'), float('inf'))
        game.undo_move()
        if eval in eval_move_dict:
            eval_move_dict[eval].append(move)
        else:
            eval_move_dict[eval] = [move]
    if game.white_to_move:
        best_eval = max(eval_move_dict.keys())
    else:
        best_eval = min(eval_move_dict.keys())

    # for e, m_list in eval_move_dict.items():
        # print(e)
        # for m in m_list:
        #     print(m.notation)

    best_move = random.choice(eval_move_dict[best_eval])

    return best_move


def positions_analyzed(game, depth):
    if depth == 0:
        return 1
    leg_moves = game.get_legal_moves()
    num_positions = 0
    for move in leg_moves:
        game.make_move(move)
        num_positions += positions_analyzed(game, depth-1)
        game.undo_move()
    return num_positions
