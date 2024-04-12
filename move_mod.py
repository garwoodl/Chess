def get_chess_notation(start, end):
    '''
    Returns the chess notation of a move in the form
    {start file}{start rank}-{end file}{end rank}
    '''
    rows_to_ranks = {0: 8, 1: 7, 2: 6, 3: 5,
                     4: 4, 5: 3, 6: 2, 7: 1}
    cols_to_files = {0: "a", 1: "b", 2: "c", 3: "d",
                     4: "e", 5: "f", 6: "g", 7: "h"}

    return cols_to_files[start[1]] + str(rows_to_ranks[start[0]]) + "-" + \
        cols_to_files[end[1]] + str(rows_to_ranks[end[0]])


def get_coord(notation: str):
    '''
    Takes a notation of the form start_square-end_square
    and returns a list of form [start coord, end coord]
    '''
    rows_to_ranks = {0: 8, 1: 7, 2: 6, 3: 5,
                     4: 4, 5: 3, 6: 2, 7: 1}
    ranks_to_rows = {v: k for k, v in rows_to_ranks.items()}
    cols_to_files = {0: "a", 1: "b", 2: "c", 3: "d",
                     4: "e", 5: "f", 6: "g", 7: "h"}
    files_to_cols = {v: k for k, v in cols_to_files.items()}

    notation = notation.split("-")
    if len(notation) == 2:
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


class Move:

    def __init__(self, start, end, cur_game, prom_piece="Q", en_passant=False):
        """
        Takes in a  {start square}-{end square} and the board
        start and end are tuples of ints representing row and col
        """
        self.notation = get_chess_notation(start, end)
        self.start = start
        self.end = end
        self.piece_moved = cur_game.board[start[0]][start[1]]
        self.piece_captured = cur_game.board[end[0]][end[1]]
        # doesn't really do anything V
        self.is_check = False

        self.is_castle = (self.piece_moved == "wK" and
                          self.start == (7, 4) and self.end == (7, 6)) or \
            (self.piece_moved == "wK" and self.start == (7, 4) and
             self.end == (7, 2)) or \
            (self.piece_moved == "bK" and self.start == (0, 4) and
             self.end == (0, 6)) or \
            (self.piece_moved == "bK" and self.start == (0, 4) and
             self.end == (0, 2))
        self.lost_castling = self.is_castle
        self.en_passant = en_passant
        # piece_placed is for promotion
        the_color = self.piece_moved[0]
        self.promotion = False
        if (self.piece_moved == "wP") and (self.end[0] == 0):
            self.promotion = True
        if (self.piece_moved == "bP") and (self.end[0] == 7):
            self.promotion = True

        if self.promotion:
            self.piece_placed = the_color + prom_piece
        else:
            self.piece_placed = self.piece_moved

    def __eq__(self, other):
        return (self.start == other.start) and (self.end == other.end) and \
            (self.piece_moved == other.piece_moved) and \
            (self.piece_placed == other.piece_placed) and \
            (self.piece_captured == other.piece_captured)

    def __str__(self):
        if self.is_check:
            check = "check"
        else:
            check = ''
        return self.piece_moved + ' ' + self.notation + ' ' + check

    def __hash__(self):
        return hash((self.piece_moved, self.piece_placed, self.piece_captured,
                    self.start, self.end))
