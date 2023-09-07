import pygame, sys

from const import *
from game import Game
from square import Square
from move import Move

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess - Created by Clayton')
        self.game = Game()

    def mainloop(self):
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger

        while True:
            # show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            game.show_hover(screen)

            if dragger.is_dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                # click event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouse_coord_y // SQUARESIZE
                    clicked_col = dragger.mouse_coord_x // SQUARESIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color) ?
                        if piece.color == game.next_player:
                            board.calculate_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial_position(event.pos)
                            dragger.drag_piece(piece)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQUARESIZE
                    motion_col = event.pos[0] // SQUARESIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.is_dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.is_dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouse_coord_y // SQUARESIZE
                        released_col = dragger.mouse_coord_x // SQUARESIZE

                        # dreate possible move
                        initial_square = Square(dragger.initial_row, dragger.initial_col)
                        final_square = Square(released_row, released_col)
                        move = Move(initial_square, final_square)

                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)

                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            game.next_turn()

                    dragger.undrag_piece()

                # key press
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        game.change_theme()

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()

main.mainloop()
