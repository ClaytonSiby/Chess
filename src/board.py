from const import *
from square import Square
from piece import *
from move import *

class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None

        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))

    def calculate_moves(self, piece, row, col):
        '''
          Calculate all the possible valid moves of a specific piece on a specific position
        '''

        def knight_moves():
            # 8 possible moves for the knight on the center of the board
            possible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1)
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_has_enemy_piece(piece.color):
                        # create squares of the new move
                        initial_square = Square(row, col)
                        final_square   = Square(possible_move_row, possible_move_col) # piece = piece

                        # create new move
                        move = Move(initial_square, final_square)

                        # add move
                        piece.add_move(move)

        def pawn_moves():
            steps = 1 if piece.moved else 2
            
            # vertical moves
            start_position = row + piece.direction
            end_postion    = row + piece.direction * (1 + steps)

            for possible_move_row in range(start_position, end_postion, piece.direction):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].is_empty():
                        # create initial and final squares
                        initial_square = Square(row, col)
                        final_square   = Square(possible_move_row, col)

                        # create a new move
                        move           = Move(initial_square, final_square)

                        # append a new move 
                        piece.add_move(move)

                    # blocked
                    else: break
                # not in range
                else: break

            # diagonal moves
            possible_move_row  = row + piece.direction
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create initial and final squares
                        initial_square = Square(row, col)
                        final_square   = Square(possible_move_row, possible_move_col)

                        # create a new move
                        move = Move(initial_square, final_square)

                        # append a new move
                        piece.add_move(move)

        def straightline_moves(increments):
            for increment in increments:
                row_increment, column_increment = increment
                possible_move_row = row + row_increment
                possible_move_col = col + column_increment

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create squares of the possible new move
                        initial_square = Square(row, col)
                        final_square   = Square(possible_move_row, possible_move_col)

                        move = Move(initial_square, final_square)

                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            # append new move
                            piece.add_move(move)

                        # has enemy piece already
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # create a new move ( add move and break )
                            piece.add_move(move)
                            break

                        # has team piece already (break)
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    else: break

                    # incrementing the increments
                    possible_move_row = possible_move_row + row_increment
                    possible_move_col = possible_move_col + column_increment

        def king_moves():
            adjacents = [
                (row - 1, col + 0), # up
                (row - 1, col + 1), # up-right
                (row + 0, col + 1), # right
                (row + 1, col + 1), # down-right
                (row + 1, col + 0), # down
                (row + 1, col - 1), # down-left
                (row + 0, col - 1), # left
                (row - 1, col - 1), # up-left
            ]

            for adjacent_move in adjacents:
                adjacent_move_row, adjacent_move_col = adjacent_move

                if Square.in_range(adjacent_move_row, adjacent_move_col):
                    if self.squares[adjacent_move_row][adjacent_move_col].is_empty_or_has_enemy_piece(piece.color):
                        # create a new move
                        initial_square = Square(row, col)
                        final_square   = Square(adjacent_move_row, adjacent_move_col)

                        # create a move
                        move = Move(initial_square, final_square)

                        # add a new valid possible move
                        piece.add_move(move)


        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            moves_for_the_bishop = [
                (-1, 1), # up right
                (-1, -1), # up left
                (1, 1), # down right
                (1, -1), # down left
            ]
            straightline_moves(moves_for_the_bishop)

        elif isinstance(piece, Rook):
            moves_for_the_rook = [
                (-1, 0), # up
                (0, 1), # right
                (1, 0), # down
                (0, -1), # left
            ]
            straightline_moves(moves_for_the_rook)

        elif isinstance(piece, Queen):
            moves_for_the_queen = [
                (-1, 1), # up right
                (-1, -1), # up left
                (1, 1), # down right
                (1, -1), # down left
                (-1, 0), # up
                (0, 1), # left
                (1, 0), # down
                (0, -1), # right
            ]
            straightline_moves(moves_for_the_queen)

        elif isinstance(piece, King):
            king_moves()

    def move(self, piece, move):
        initial_square = move.initial_square
        final_square = move.final_square

        self.squares[initial_square.row][initial_square.col].piece = None
        self.squares[final_square.row][final_square.col].piece = piece

        # move pieces
        piece.moved = True

        # clear valid moves after changing position
        piece.clear_moves()

        self.last_move = move


    def valid_move(self, piece, move):
        return move in piece.valued_moves
