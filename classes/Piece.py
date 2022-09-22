import pygame
import pygame.gfxdraw

PIECE_IMG = pygame.Surface((30,30), pygame.SRCALPHA)


class Piece(pygame.sprite.Sprite):
    def __init__(self, color, pos_x, pos_y, troops, id):
        super().__init__()
        self.id = id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.troops = troops
        self.radius = 15
        self.frame = pygame.Surface((30,30), pygame.SRCALPHA)
        pygame.draw.circle(self.frame, color, (self.radius, self.radius), self.radius, 0)
        self.rect = self.frame.get_rect()
        self.rect.center = (pos_x, pos_y)