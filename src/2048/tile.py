import pygame
from colors import COLORS

class Tile:
    def __init__(self, position, value, side):
        pygame.font.init()
        self.position = position
        self.value = value
        self.tile_side = side
        self.font = pygame.font.SysFont('arialrounded', 30)

    def update_features(self):
        self.text = str(2 ** self.value)
        self.background_color, self.text_color = COLORS[min(self.value, 12)]
        self.label = self.font.render(self.text, 1, self.text_color)
        self.x = self.position[1] * self.tile_side + self.tile_side // 2 - self.label.get_width() // 2
        self.y = self.position[0] * self.tile_side + self.tile_side // 2 - self.label.get_height() // 2

    def update_value(self, new_value):
        self.value = new_value

    def show(self, surface):
        self.update_features()
        pygame.draw.rect(surface, self.background_color, (self.position[1]*self.tile_side, self.position[0]*self.tile_side, self.tile_side, self.tile_side))
        surface.blit(self.label, (self.x, self.y))