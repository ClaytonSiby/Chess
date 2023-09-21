import pygame
 
from const import *

class Dragger:
    def __init__(self):
        self.piece = None
        self.is_dragging = False
        self.mouse_coord_x = 0
        self.mouse_coord_y = 0
        self.initial_row = 0
        self.initial_col = 0

    def update_blit(self, surface):
        self.piece.set_texture(size = 128) # texture
        texture = self.piece.texture # path to the image
    
        img = pygame.image.load(texture) # create the image
        img_center = (self.mouse_coord_x, self.mouse_coord_y) # center
        self.piece.texture_rect = img.get_rect(center = img_center)

        # blit
        surface.blit(img, self.piece.texture_rect)

    def update_mouse(self, position):
        self.mouse_coord_x, self.mouse_coord_y = position # (xcor, ycor)
    
    def save_initial_position(self, position):
        self.initial_row = position[1] // SQUARESIZE
        self.initial_col = position[0] // SQUARESIZE


    def drag_piece(self, piece):
        self.piece = piece
        self.is_dragging = True

    def undrag_piece(self):
        self.piece = None
        self.is_dragging = False

