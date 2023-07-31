import pygame

from const import *
from board import Board
from dragger import Dragger

class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()

    # drawing the game
    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200) # light green
                else:
                    color = (119, 154, 88)  # dark green

                rectangle = (col * SQUARESIZE, row * SQUARESIZE, SQUARESIZE, SQUARESIZE)

                pygame.draw.rect(surface, color, rectangle)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    img = pygame.image.load(piece.texture)
                    img_center = col * SQUARESIZE + SQUARESIZE // 2 , row * SQUARESIZE + SQUARESIZE // 2

                    piece.texture_rect = img.get_rect(center = img_center)
                    surface.blit(img, piece.texture_rect)

