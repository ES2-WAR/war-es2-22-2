import pygame
import pygame.gfxdraw

from classes.Territory import *

PIECE_IMG = pygame.Surface((30,30), pygame.SRCALPHA)
COLORS = { 
  'branco': (255,255,255),
  'vermelho': (255,0,0),
  'verde': (0,255,0),
  'azul': (0,0,255),
  'preto': (0,0,0)
}


class Piece(pygame.sprite.Sprite):
  def __init__(self, territoryColor: str, pos_x: int, pos_y: int, troops: int, territoryId: int):
    super().__init__()
    self.territoryId = territoryId
    self.pos_x = pos_x
    self.pos_y = pos_y
    self.troops = troops
    self.radius = 15
    self.frame = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
    pygame.draw.circle(self.frame, COLORS[territoryColor], (self.radius, self.radius), self.radius, 0)
    self.rect = self.frame.get_rect()
    self.rect.center = (pos_x, pos_y)
  
  def updatePiece(self, relatedTerritory: Territory):
    self.troops = relatedTerritory.numberOfTroops
    pygame.draw.circle(self.frame, COLORS[relatedTerritory.color], (self.radius, self.radius), self.radius, 0)
