"""
Board Class and Move Class
Handles how the game works
"""
from move_mod import Move


def str_to_board(s):
    """
    takes in a string of length 128 and sets the board to that string
    """
    new_board = [
        [], [], [], [], [], [], [], []
    ]
    i = 0
    for row in range(8):
        for _ in range(8):
            new_board[row].append(s[i: i + 2])
            i += 2
    return new_board


class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        # self.board = [
        #     ["--", "--", "--", "--", "--", "--", "--", "bR"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "wB", "--", "bP", "--"],
        #     ["--", "--", "--", "--", "--", "--", "wP", "wP"],
        #     ["--", "--", "--", "--", "--", "bK", "--", "wK"],
        # ]
        # self.board = [
        #     ["--", "bR", "--", "--", "bK", "--", "--", "--"],
        #     ["--", "bR", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "wP", "--"],
        #     ["--", "bQ", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "wB", "--", "--", "--", "--"],
        #     ["--", "--", "--", "wP", "wP", "wP", "--", "--"],
        #     ["wR", "--", "--", "--", "wK", "--", "--", "--"],
        # ]
        # self.board = [
        #     ["bR", "--", "--", "--", "bK", "--", "--", "bR"],
        #     ["bP", "bP", "--", "--", "--", "--", "bP", "bP"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["wP", "wP", "--", "--", "--", "--", "wP", "wP"],
        #     ["wR", "--", "--", "--", "wK", "--", "--", "wR"],
        # ]
        self.white_to_move = True
        self.move_log = []
        self.game_status = "game not over"
        self.game_over = False
        self.board_str = self.board_to_str()
        self.board_log_list = [self.board_str]
        # these will keep track of if a king or rook has
        # moved already or already castled
        self.white_can_castle = True
        self.black_can_castle = True
        self.white_is_castled = False
        self.black_is_castled = False
        # self.en_passant_target = None
        self.en_passant_target_log = [None]

    def __eq__(self, other):
        """
        Two GameState objects are equal if their position is the same
        """
        return (self.board == other.board) and \
            (self.white_to_move == other.white_to_move) and \
            (self.game_over == other.game_over)

    def board_to_str(self):
        """
        Returns the board position as a full string
        """
        s = ''
        for row in self.board:
            for piece in row:
                s += piece
        return s

    def make_move(self, move):
        """
        Changes the board to show a move that was made. Updates move log
        Used in main to actually do a move
        """

        self.board[move.start[0]][move.start[1]] = "--"
        self.board[move.end[0]][move.end[1]] = move.piece_placed

        # en passant
        if (move.piece_moved[1] == 'P' and
           move.end == self.en_passant_target_log[-1]):
            # remove captured pawn
            captured_sq = (move.start[0], move.end[1])
            # move.piece_captured = self.board[captured_sq[0]][captured_sq[1]]
            self.board[captured_sq[0]][captured_sq[1]] = '--'
            move.en_passant = True
            self.en_passant_target_log.append(None)
        elif (move.piece_moved[1] == "P" and
              abs(move.start[0] - move.end[0]) == 2):
            targ = ((move.start[0] + move.end[0]) // 2, move.start[1])
            # self.en_passant_target = ((move.start[0] + move.end[0]) // 2,
            #                           move.start[1])
            self.en_passant_target_log.append(targ)
        else:
            # print("impossible en passant")
            # self.en_passant_target = None
            self.en_passant_target_log.append(None)

        # print(self.en_passant_target_log)

        self.move_log.append(move)
        if move.piece_moved[1] == "K" or move.piece_moved[1] == "R":
            self.check_and_do_castle(move)

        self.board_str = self.board_to_str()
        self.board_log_list.append(self.board_str)

        self.white_to_move = not self.white_to_move

    def undo_move(self):
        """
        Undoes the last move made
        """
        if len(self.move_log) > 0:
            last_move = self.move_log[-1]
            last_board = self.board_log_list[-2]
            last_move_color = last_move.piece_moved[0]

            if last_move.lost_castling:
                if last_move_color == "w":
                    self.white_can_castle = True
                else:
                    self.black_can_castle = True
            if last_move.is_castle:
                if last_move_color == "w":
                    self.white_is_castled = False
                else:
                    self.black_is_castled = False

            # if last_move.en_passant:
            #     self.en_passant_target = last_move.end
            # else:
                # print("can't en passant")
                # self.en_passant_target = None

            self.board = str_to_board(last_board)
            if len(self.en_passant_target_log) > 1:
                del self.en_passant_target_log[-1]
            del self.move_log[-1]
            del self.board_log_list[-1]
            self.white_to_move = not self.white_to_move

    def check_and_do_castle(self, move):
        """
        Plays the mechanics of a castle
        Turns off can castle for other king or rook moves
        """
        if (move.piece_moved == "wK" and move.start == (7, 4) and
           self.white_can_castle):
            if move.end == (7, 6):
                self.board[7][7] = "--"
                self.board[7][5] = "wR"
                self.white_is_castled = True
            elif move.end == (7, 2):
                self.board[7][0] = "--"
                self.board[7][3] = "wR"
                self.white_is_castled = True
            self.white_can_castle = False
            move.lost_castling = True
        elif (move.piece_moved == "bK" and move.start == (0, 4) and
              self.black_can_castle):
            if move.end == (0, 6):
                self.board[0][7] = "--"
                self.board[0][5] = "bR"
                self.black_is_castled = True
            elif move.end == (0, 2):
                self.board[0][0] = "--"
                self.board[0][3] = "bR"
                self.black_is_castled = True
            self.black_can_castle = False
            move.lost_castling = True
        if (move.piece_moved == "wR" and (move.start == (7, 7) or
                                          move.start == (7, 0))):
            self.white_can_castle = False
            move.lost_castling = True
        if (move.piece_moved == "bR" and (move.start == (0, 7) or
                                          move.start == (0, 0))):
            self.black_can_castle = False
            move.lost_castling = True

    def display_own_board(self):
        for r in range(8):
            for c in range(8):
                print(self.board[r][c], end=" ")
            print()

    def update_game_status(self):
        """
        returns either "White Won by Checkmate", "Black Won by Checkmate",
        "Stalemate", or "game not over"
        """
        if len(self.move_log) >= 0:
            freq_dict = {}
            for s in self.board_log_list:
                if s in freq_dict:
                    freq_dict[s] += 1
                else:
                    freq_dict[s] = 1
            if len(freq_dict) > 0:
                if max(freq_dict.values()) >= 3:
                    self.game_status = "Draw by Repetition"

            moves = self.get_legal_moves()
            if len(moves) == 0:
                if self.white_to_move:
                    self.white_to_move = False
                    blacks_next_moves = self.get_legal_moves()
                    # checks if the king can be taken next move
                    for move in blacks_next_moves:
                        if move.piece_captured[1] == "K":
                            self.white_to_move = True
                            self.game_status = "Black Won by Checkmate"
                            break
                    if not self.white_to_move:
                        self.white_to_move = True
                        self.game_status = "Stalemate"
                else:
                    self.white_to_move = True
                    whites_next_moves = self.get_legal_moves()
                    for move in whites_next_moves:
                        if move.piece_captured[1] == "K":
                            self.white_to_move = False
                            self.game_status = "White Won by Checkmate"
                            break
                    if self.white_to_move:
                        self.white_to_move = False
                        self.game_status = "Stalemate"
            else:
                pieces_left = set()
                for r in range(8):
                    for c in range(8):
                        pieces_left.add(self.board[r][c])
                if len(pieces_left) == 3:
                    self.game_status = "Draw"
            self.game_over = (self.game_status == "White Won by Checkmate") or\
                (self.game_status == "Black Won by Checkmate") or \
                (self.game_status == "Stalemate") or \
                (self.game_status == "Draw") or \
                (self.game_status == "Draw by Repetition")

    def get_legal_moves(self):
        """
        Returns a final list of legal moves
        """
        # if on next move, taking King is legal, then this move is illegal
        moves = self.get_almost_legal_moves()
        moves_w_no_check = []

        for move in moves:
            move_invalid = False
            self.make_move(move)
            next_moves = self.get_almost_legal_moves()
            # for n in next_moves:
            #     # marks checks
            #     self.white_to_move = not self.white_to_move
            #     if (n.piece_captured[1] == "K"):
            #         move.is_check = True
            #     self.white_to_move = not self.white_to_move

            self.undo_move()

            for m in next_moves:
                # checks if move puts us into check
                if m.piece_captured[1] == "K":
                    move_invalid = True
                    break  # this was commented out but idk why
            if move.is_castle:
                illegal_castles = self.get_illegal_castles(move, next_moves)
                for c in illegal_castles:
                    if c in moves:
                        move_invalid = True
                        break

            if not move_invalid:
                moves_w_no_check.append(move)

        return moves_w_no_check

    def get_illegal_castles(self, move, next_moves):
        """
        Move is a potentially legal move without considering checks
        Next moves is a list of what white could do next after the move
        Returns a list of illegal castles
        """
        illegal_moves = []
        if move.is_castle:
            if self.white_to_move and self.white_can_castle:
                if move == Move((7, 4), (7, 6), self):
                    for n in next_moves:
                        if ((n.end == (7, 4)) or (n.end == (7, 5)) or
                           (n.end == (7, 6))):
                            illegal_moves.append(move)
                            break
                elif move == Move((7, 4), (7, 2), self):
                    for n in next_moves:
                        if ((n.end == (7, 4)) or (n.end == (7, 3)) or
                           (n.end == (7, 2))):
                            illegal_moves.append(move)
                            break
            elif (not self.white_to_move) and self.black_can_castle:
                if move == Move((0, 4), (0, 6), self):
                    for n in next_moves:
                        if ((n.end == (0, 4)) or (n.end == (0, 5)) or
                           (n.end == (0, 6))):
                            illegal_moves.append(move)
                            break
                elif move == Move((0, 4), (0, 2), self):
                    for n in next_moves:
                        if ((n.end == (0, 4)) or (n.end == (0, 3)) or
                           (n.end == (0, 2))):
                            illegal_moves.append(move)
                            break

        return illegal_moves

    def get_almost_legal_moves(self):
        """
        Returns a list of legal moves not including checks or
        en passant or castling
        """
        moves = []
        if self.white_to_move:  # white moves
            for r in range(8):
                for c in range(8):
                    color = self.board[r][c][0]
                    if color == "w":
                        piece = self.board[r][c][1]
                        if piece == "P":
                            self.get_white_pawns_moves(r, c, moves)
                        if piece == "B":
                            self.get_bishops_moves(r, c, moves)
                        if piece == "N":
                            self.get_knights_moves(r, c, moves)
                        if piece == "R":
                            self.get_rooks_moves(r, c, moves)
                        if piece == "Q":
                            self.get_queens_moves(r, c, moves)
                        if piece == "K":
                            self.get_kings_moves(r, c, moves)

        else:  # black moves
            for r in range(8):
                for c in range(8):
                    color = self.board[r][c][0]
                    if color == "b":
                        piece = self.board[r][c][1]
                        if piece == "P":
                            self.get_black_pawns_moves(r, c, moves)
                        if piece == "B":
                            self.get_bishops_moves(r, c, moves)
                        if piece == "N":
                            self.get_knights_moves(r, c, moves)
                        if piece == "R":
                            self.get_rooks_moves(r, c, moves)
                        if piece == "Q":
                            self.get_queens_moves(r, c, moves)
                        if piece == "K":
                            self.get_kings_moves(r, c, moves)
        return moves

    def get_white_pawns_moves(self, r, c, moves):
        if self.board[r - 1][c] == "--":
            moves.append(Move((r, c), (r-1, c), self))
            if r == 6:
                if self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self))
        if c > 0:
            if self.en_passant_target_log[-1] == (r-1, c-1):
                moves.append(Move((r, c), (r-1, c-1), self, en_passant=True))
            if self.board[r - 1][c - 1][0] == "b":  # black piece to left diag
                moves.append(Move((r, c), (r-1, c-1), self, en_passant=True))
        if c < 7:
            if self.en_passant_target_log[-1] == (r-1, c+1):
                moves.append(Move((r, c), (r-1, c+1), self))
            if self.board[r - 1][c + 1][0] == "b":  # right diag
                moves.append(Move((r, c), (r-1, c+1), self))

    def get_black_pawns_moves(self, r, c, moves):
        if self.board[r + 1][c] == "--":
            moves.append(Move((r, c), (r+1, c), self))
            if r == 1:
                if self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self))
        if c > 0:
            if self.en_passant_target_log[-1] == (r+1, c-1):
                moves.append(Move((r, c), (r+1, c-1), self, en_passant=True))
            if self.board[r + 1][c - 1][0] == "w":  # black piece to left diag
                moves.append(Move((r, c), (r+1, c-1), self))
        if c < 7:
            if self.en_passant_target_log[-1] == (r+1, c+1):
                moves.append(Move((r, c), (r+1, c+1), self, en_passant=True))
            if self.board[r + 1][c + 1][0] == "w":  # right diag
                moves.append(Move((r, c), (r+1, c+1), self))

    def get_bishops_moves(self, r, c, moves):
        bish_color = self.board[r][c][0]
        if bish_color == "w":
            other_color = "b"
        else:
            other_color = "w"

        # check right up diag
        check_r = r
        check_c = c
        in_bounds = (0 <= check_r) and (check_r <= 7) and \
            (0 <= check_c) and (check_c <= 7)
        open_lane = True
        while in_bounds and open_lane:
            check_r -= 1
            check_c += 1
            in_bounds = (0 <= check_r) and (check_r <= 7) and \
                (0 <= check_c) and (check_c <= 7)
            if in_bounds:
                if self.board[check_r][check_c] == "--":
                    moves.append(Move((r, c), (check_r, check_c), self))
                elif self.board[check_r][check_c][0] == other_color:
                    moves.append(Move((r, c), (check_r, check_c), self))
                    open_lane = False
                else:
                    open_lane = False
        # check left up diag
        check_r = r
        check_c = c
        in_bounds = (0 <= check_r) and (check_r <= 7) and (0 <= check_c) and \
            (check_c <= 7)
        open_lane = True
        while in_bounds and open_lane:
            check_r -= 1
            check_c -= 1
            in_bounds = (0 <= check_r) and (check_r <= 7) and \
                (0 <= check_c) and (check_c <= 7)
            if in_bounds:
                if self.board[check_r][check_c] == "--":
                    moves.append(Move((r, c), (check_r, check_c), self))
                elif self.board[check_r][check_c][0] == other_color:
                    moves.append(Move((r, c), (check_r, check_c), self))
                    open_lane = False
                else:
                    open_lane = False
        # check right down diag
        check_r = r
        check_c = c
        in_bounds = (0 <= check_r) and (check_r <= 7) and (0 <= check_c) and \
            (check_c <= 7)
        open_lane = True
        while open_lane and in_bounds:
            check_r += 1
            check_c += 1
            in_bounds = (0 <= check_r) and (check_r <= 7) and \
                (0 <= check_c) and (check_c <= 7)
            if in_bounds:
                if self.board[check_r][check_c] == "--":
                    moves.append(Move((r, c), (check_r, check_c), self))
                elif self.board[check_r][check_c][0] == other_color:
                    moves.append(Move((r, c), (check_r, check_c), self))
                    open_lane = False
                else:
                    open_lane = False
        # check left down diag
        check_r = r
        check_c = c
        in_bounds = (0 <= check_r) and (check_r <= 7) and (0 <= check_c) and \
            (check_c <= 7)
        open_lane = True
        while in_bounds and open_lane:
            check_r += 1
            check_c -= 1
            in_bounds = (0 <= check_r) and (check_r <= 7) and \
                (0 <= check_c) and (check_c <= 7)
            if in_bounds:
                if self.board[check_r][check_c] == "--":
                    moves.append(Move((r, c), (check_r, check_c), self))
                elif self.board[check_r][check_c][0] == other_color:
                    moves.append(Move((r, c), (check_r, check_c), self))
                    open_lane = False
                else:
                    open_lane = False

    def get_knights_moves(self, r, c, moves):
        knight_color = self.board[r][c][0]
        if knight_color == "w":
            other_color = "b"
        else:
            other_color = "w"

        possible_lands = [
            (r-2, c+1), (r-1, c+2), (r+1, c+2), (r+2, c+1),
            (r+2, c-1), (r+1, c-2), (r-1, c-2), (r-2, c-1)
        ]
        for square in possible_lands:
            in_bound = (0 <= square[0]) and (square[0] <= 7) and \
                (0 <= square[1]) and (square[1] <= 7)
            if in_bound:
                piece_color = self.board[square[0]][square[1]][0]
                if piece_color == "-" or piece_color == other_color:
                    moves.append(Move((r, c), (square[0], square[1]), self))

    def get_rooks_moves(self, r, c, moves):
        rook_color = self.board[r][c][0]
        if rook_color == "w":
            other_color = "b"
        else:
            other_color = "w"
        # check up
        check_r = r
        check_c = c
        in_bounds = (0 <= check_r) and (check_r <= 7) and \
            (0 <= check_c) and (check_c <= 7)
        open_lane = True
        while in_bounds and open_lane:
            check_r -= 1
            in_bounds = (0 <= check_r) and (check_r <= 7) and \
                (0 <= check_c) and (check_c <= 7)
            if in_bounds:
                if self.board[check_r][check_c] == "--":
                    moves.append(Move((r, c), (check_r, check_c), self))
                elif self.board[check_r][check_c][0] == other_color:
                    moves.append(Move((r, c), (check_r, check_c), self))
                    open_lane = False
                else:
                    open_lane = False
        # check right
        check_r = r
        check_c = c
        in_bounds = (0 <= check_r) and (check_r <= 7) and (0 <= check_c) and \
            (check_c <= 7)
        open_lane = True
        while in_bounds and open_lane:
            check_c += 1
            in_bounds = (0 <= check_r) and (check_r <= 7) and \
                (0 <= check_c) and (check_c <= 7)
            if in_bounds:
                if self.board[check_r][check_c] == "--":
                    moves.append(Move((r, c), (check_r, check_c), self))
                elif self.board[check_r][check_c][0] == other_color:
                    moves.append(Move((r, c), (check_r, check_c), self))
                    open_lane = False
                else:
                    open_lane = False
        # check down
        check_r = r
        check_c = c
        in_bounds = (0 <= check_r) and (check_r <= 7) and (0 <= check_c) and \
            (check_c <= 7)
        open_lane = True
        while open_lane and in_bounds:
            check_r += 1
            in_bounds = (0 <= check_r) and (check_r <= 7) and \
                (0 <= check_c) and (check_c <= 7)
            if in_bounds:
                if self.board[check_r][check_c] == "--":
                    moves.append(Move((r, c), (check_r, check_c), self))
                elif self.board[check_r][check_c][0] == other_color:
                    moves.append(Move((r, c), (check_r, check_c), self))
                    open_lane = False
                else:
                    open_lane = False
        # check left
        check_r = r
        check_c = c
        in_bounds = (0 <= check_r) and (check_r <= 7) and (0 <= check_c) and \
            (check_c <= 7)
        open_lane = True
        while in_bounds and open_lane:
            check_c -= 1
            in_bounds = (0 <= check_r) and (check_r <= 7) and \
                (0 <= check_c) and (check_c <= 7)
            if in_bounds:
                if self.board[check_r][check_c] == "--":
                    moves.append(Move((r, c), (check_r, check_c), self))
                elif self.board[check_r][check_c][0] == other_color:
                    moves.append(Move((r, c), (check_r, check_c), self))
                    open_lane = False
                else:
                    open_lane = False

    def get_queens_moves(self, r, c, moves):
        queen_color = self.board[r][c][0]
        if queen_color == "w":
            other_color = "b"
        else:
            other_color = "w"
        # check right up diag
        check_r = r
        check_c = c
        in_bounds = (0 <= check_r) and (check_r <= 7) and \
            (0 <= check_c) and (check_c <= 7)
        open_lane = True
        while in_bounds and open_lane:
            check_r -= 1
            check_c += 1
            in_bounds = (0 <= check_r) and (check_r <= 7) and \
                (0 <= check_c) and (check_c <= 7)
            if in_bounds:
                if self.board[check_r][check_c] == "--":
                    moves.append(Move((r, c), (check_r, check_c), self))
                elif self.board[check_r][check_c][0] == other_color:
                    moves.append(Move((r, c), (check_r, check_c), self))
                    open_lane = False
                else:
                    open_lane = False
        # check left up diag
        check_r = r
        check_c = c
        in_bounds = (0 <= check_r) and (check_r <= 7) and (0 <= check_c) and \
            (check_c <= 7)
        open_lane = True
        while in_bounds and open_lane:
            check_r -= 1
            check_c -= 1
            in_bounds = (0 <= check_r) and (check_r <= 7) and \
                (0 <= check_c) and (check_c <= 7)
            if in_bounds:
                if self.board[check_r][check_c] == "--":
                    moves.append(Move((r, c), (check_r, check_c), self))
                elif self.board[check_r][check_c][0] == other_color:
                    moves.append(Move((r, c), (check_r, check_c), self))
                    open_lane = False
                else:
                    open_lane = False
        # check right down diag
        check_r = r
        check_c = c
        in_bounds = (0 <= check_r) and (check_r <= 7) and (0 <= check_c) and \
            (check_c <= 7)
        open_lane = True
        while open_lane and in_bounds:
            check_r += 1
            check_c += 1
            in_bounds = (0 <= check_r) and (check_r <= 7) and \
                (0 <= check_c) and (check_c <= 7)
            if in_bounds:
                if self.board[check_r][check_c] == "--":
                    moves.append(Move((r, c), (check_r, check_c), self))
                elif self.board[check_r][check_c][0] == other_color:
                    moves.append(Move((r, c), (check_r, check_c), self))
                    open_lane = False
                else:
                    open_lane = False
        # check left down diag
        check_r = r
        check_c = c
        in_bounds = (0 <= check_r) and (check_r <= 7) and (0 <= check_c) and \
            (check_c <= 7)
        open_lane = True
        while in_bounds and open_lane:
            check_r += 1
            check_c -= 1
            in_bounds = (0 <= check_r) and (check_r <= 7) and \
                (0 <= check_c) and (check_c <= 7)
            if in_bounds:
                if self.board[check_r][check_c] == "--":
                    moves.append(Move((r, c), (check_r, check_c), self))
                elif self.board[check_r][check_c][0] == other_color:
                    moves.append(Move((r, c), (check_r, check_c), self))
                    open_lane = False
                else:
                    open_lane = False
        # check up
        check_r = r
        check_c = c
        in_bounds = (0 <= check_r) and (check_r <= 7) and \
            (0 <= check_c) and (check_c <= 7)
        open_lane = True
        while in_bounds and open_lane:
            check_r -= 1
            in_bounds = (0 <= check_r) and (check_r <= 7) and \
                (0 <= check_c) and (check_c <= 7)
            if in_bounds:
                if self.board[check_r][check_c] == "--":
                    moves.append(Move((r, c), (check_r, check_c), self))
                elif self.board[check_r][check_c][0] == other_color:
                    moves.append(Move((r, c), (check_r, check_c), self))
                    open_lane = False
                else:
                    open_lane = False
        # check right
        check_r = r
        check_c = c
        in_bounds = (0 <= check_r) and (check_r <= 7) and (0 <= check_c) and \
            (check_c <= 7)
        open_lane = True
        while in_bounds and open_lane:
            check_c += 1
            in_bounds = (0 <= check_r) and (check_r <= 7) and \
                (0 <= check_c) and (check_c <= 7)
            if in_bounds:
                if self.board[check_r][check_c] == "--":
                    moves.append(Move((r, c), (check_r, check_c), self))
                elif self.board[check_r][check_c][0] == other_color:
                    moves.append(Move((r, c), (check_r, check_c), self))
                    open_lane = False
                else:
                    open_lane = False
        # check down
        check_r = r
        check_c = c
        in_bounds = (0 <= check_r) and (check_r <= 7) and (0 <= check_c) and \
            (check_c <= 7)
        open_lane = True
        while open_lane and in_bounds:
            check_r += 1
            in_bounds = (0 <= check_r) and (check_r <= 7) and \
                (0 <= check_c) and (check_c <= 7)
            if in_bounds:
                if self.board[check_r][check_c] == "--":
                    moves.append(Move((r, c), (check_r, check_c), self))
                elif self.board[check_r][check_c][0] == other_color:
                    moves.append(Move((r, c), (check_r, check_c), self))
                    open_lane = False
                else:
                    open_lane = False
        # check left
        check_r = r
        check_c = c
        in_bounds = (0 <= check_r) and (check_r <= 7) and (0 <= check_c) and \
            (check_c <= 7)
        open_lane = True
        while in_bounds and open_lane:
            check_c -= 1
            in_bounds = (0 <= check_r) and (check_r <= 7) and \
                (0 <= check_c) and (check_c <= 7)
            if in_bounds:
                if self.board[check_r][check_c] == "--":
                    moves.append(Move((r, c), (check_r, check_c), self))
                elif self.board[check_r][check_c][0] == other_color:
                    moves.append(Move((r, c), (check_r, check_c), self))
                    open_lane = False
                else:
                    open_lane = False

    def get_kings_moves(self, r, c, moves):
        king_color = self.board[r][c][0]
        if king_color == "w":
            other_color = "b"
        else:
            other_color = "w"

        if king_color == "w" and self.white_can_castle:
            if r == 7 and c == 4:
                if (self.board[r][c+1] == "--" and self.board[r][c+2] == "--"
                   and self.board[r][c+3] == "wR"):
                    moves.append(Move((r, c), (r, c+2), self))
                if (self.board[r][c-1] == "--" and
                   self.board[r][c-2] == "--" and self.board[r][c-3] == "--"
                   and self.board[r][c-4] == "wR"):
                    moves.append(Move((r, c), (r, c-2), self))
        if king_color == "b" and self.black_can_castle:
            if r == 0 and c == 4:
                if (self.board[r][c+1] == "--" and self.board[r][c+2] == "--"
                   and self.board[r][c+3] == "bR"):
                    moves.append(Move((r, c), (r, c+2), self))
                if (self.board[r][c-1] == "--" and
                   self.board[r][c-2] == "--" and self.board[r][c-3] == "--"
                   and self.board[r][c-4] == "bR"):
                    moves.append(Move((r, c), (r, c-2), self))

        possible_lands = [
            (r-1, c+1), (r-1, c), (r-1, c-1), (r, c-1),
            (r, c+1), (r+1, c-1), (r+1, c), (r+1, c+1)
        ]
        for square in possible_lands:
            in_bound = (0 <= square[0]) and (square[0] <= 7) and \
                (0 <= square[1]) and (square[1] <= 7)
            if in_bound:
                piece_color = self.board[square[0]][square[1]][0]
                if piece_color == "-" or piece_color == other_color:
                    moves.append(Move((r, c), (square[0], square[1]), self))
