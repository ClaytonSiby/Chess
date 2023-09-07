import pygame

from const import *
from board import Board
from dragger import Dragger
from config import Config

class Game:
    def __init__(self):
        self.next_player = 'white'
        self.hovered_square = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    # drawing the game
    def show_bg(self, surface):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                color = theme.background_color.light if (row + col) % 2 == 0 else theme.background_color.dark

                rectangle = (col * SQUARESIZE, row * SQUARESIZE, SQUARESIZE, SQUARESIZE)

                pygame.draw.rect(surface, color, rectangle)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQUARESIZE + SQUARESIZE // 2 , row * SQUARESIZE + SQUARESIZE // 2

                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect)

    
    def show_moves(self, surface):
        theme = self.config.theme

        if self.dragger.is_dragging:
            piece = self.dragger.piece

            # loop and blit valued moves
            for move in piece.valued_moves:
                # color
                color = theme.moves.light if (move.final_square.row + move.final_square.col) % 2 == 0 else theme.moves.dark
                # rect
                rectangle = (move.final_square.col * SQUARESIZE, move.final_square.row * SQUARESIZE, SQUARESIZE, SQUARESIZE)
                # blit
                pygame.draw.rect(surface, color, rectangle)

    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial_square = self.board.last_move.initial_square
            final_square = self.board.last_move.final_square

            for position in [initial_square, final_square]:
                # set color
                color = theme.trace.light if (position.row + position.col) % 2 == 0 else theme.trace.dark
                # rect
                rectangle = (position.col * SQUARESIZE, position.row * SQUARESIZE, SQUARESIZE, SQUARESIZE)
                # blit
                pygame.draw.rect(surface, color, rectangle)

    def show_hover(self, surface):
        if self.hovered_square:
            color = (180, 180, 180)
            # rect
            rectangle = (self.hovered_square.col * SQUARESIZE, self.hovered_square.row * SQUARESIZE, SQUARESIZE, SQUARESIZE)
            # blit
            pygame.draw.rect(surface, color, rectangle, width=3)

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_square = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()
