"""
Runs the user interface and displays board
"""
from game_mod import GameState
from move_mod import Move
import evaluation as eval
import time


def display_board(state: GameState()):
    for r in range(8):
        for c in range(8):
            print(state.board[r][c], end=" ")
        print()


def get_coord(notation: str):
    '''
    Takes a notation of the form start_square-end_square
    and returns a list of form [start coord, end coord]
    '''
    rows_to_ranks = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
    ranks_to_rows = {v: k for k, v in rows_to_ranks.items()}
    cols_to_files = {0: "a", 1: "b", 2: "c", 3: "d",
                     4: "e", 5: "f", 6: "g", 7: "h"}
    files_to_cols = {v: k for k, v in cols_to_files.items()}

    notation = notation.split("-")
    if (len(notation) == 2):
        start_square = notation[0]
        end_square = notation[1]
    else:
        print("NOTATION LENGTH ERROR")

    start_file = start_square[0]
    start_rank = int(start_square[1])
    end_file = end_square[0]
    end_rank = int(end_square[1])

    start = (ranks_to_rows[start_rank], files_to_cols[start_file])
    end = (ranks_to_rows[end_rank], files_to_cols[end_file])

    return [start, end]


def get_response(game: GameState):
    '''
    Asks for a response and user friendly checks it until it is valid
    Returns the notation
    '''
    ranks = set(["1", "2", "3", "4", "5", "6", "7", "8"])
    files = set(["a", "b", "c", "d", "e", "f", "g", "h"])
    if (game.white_to_move):
        color = "White"
    else:
        color = "Black"
    valid_response = False
    while (not valid_response):
        print(f"{color} to move:")
        response = input()
        if (response == "q" or response == "u"):
            return response
        if (len(response) == 5):
            if (response[2] == "-"):
                if (response[0] in files and response[1] in ranks):
                    if (response[3] in files and response[4] in ranks):
                        return response
        print("Not a valid response")


def player_vs_bot(game):
    while not game.game_over:
        # for n in eval.order_moves(game.get_legal_moves()):
        #     print(n)
        if game.white_to_move:
            print(f"There are {len(game.get_legal_moves())} legal moves.")
            response = get_response(game)
            if response == "q":
                game.game_over = True
                break
            elif response == "u":
                game.undo_move()
                game.undo_move()  # when playing a bot
                display_board(game)
            else:
                start, end = get_coord(response)
                move = Move(start, end, game)
                if move in game.get_legal_moves():
                    game.make_move(move)
                    display_board(game)
                else:
                    print("Illegal move")
        else:
            # move = eval.random_bot(game)
            # move = eval.min_legal_moves_bot(game)
            # move = eval.min_net_legal_moves_bot(game)
            # move = eval.avoid_blunder_bot(game)
            # move = eval.material_bot(game)
            move = eval.deep_bot(game, 3)
            # ordered_moves = eval.order_moves(game.get_legal_moves())
            # for m in ordered_moves:
            #     print(m)
            game.make_move(move)
            print(f"Black plays {move.notation}")
            display_board(game)
        print(eval.get_evaluation(game))
        game.update_game_status()

    print(f"Game lasted {len(game.move_log)} moves")
    return game.game_status


def player_vs_player(game):
    while (not game.game_over):
        leg = game.get_legal_moves()
        print(f"There are {len(leg)} legal moves.")
        # for m in game.get_legal_moves():
        #     print(m)
        response = get_response(game)
        if (response == "q"):
            game.game_over = True
            break
        elif (response == "u"):
            game.undo_move()
            display_board(game)
        else:
            start, end = get_coord(response)
            move = Move(start, end, game)
            print(move)
            print(move in leg)
            if (move in leg):
                game.make_move(move)
                display_board(game)
            else:
                print("Illegal move")
        print(eval.get_evaluation(game))
        game.update_game_status()

    print(f"Game lasted {len(game.move_log)} moves")
    return game.game_status


def bot_vs_bot(game):
    while (not game.game_over):
        if (game.white_to_move):
            # move = eval.min_legal_moves_bot(game)
            # move = eval.min_net_legal_moves_bot(game)
            # move = eval.random_bot(game)
            # move = eval.material_bot(game)
            # move = eval.avoid_blunder_bot(game)
            move = eval.deep_bot(game, 3)
            game.make_move(move)
            print(f"White plays {move}")
            display_board(game)
        else:
            # move = eval.random_bot(game)
            # move = eval.min_net_legal_moves_bot(game)
            # move = eval.min_legal_moves_bot(game)
            # move = eval.avoid_blunder_bot(game)
            move = eval.deep_bot(game, 2)
            game.make_move(move)
            print(f"Black plays {move}")
            display_board(game)
        print(eval.get_evaluation(game))
        game.update_game_status()

    print(f"Game lasted {len(game.move_log)} moves")
    return game.game_status


def check_positions(game, depth):
    tic = time.perf_counter()
    print(eval.positions_analyzed(game, depth))
    toc = time.perf_counter()
    print(f"{toc - tic:0.6f} seconds")


def main():
    game = GameState()
    display_board(game)
    # check_positions(game, 4)
    # game_status = player_vs_bot(game)
    game_status = bot_vs_bot(game)
    # game_status = player_vs_player(game)
    print(game_status)


if __name__ == "__main__":
    main()
