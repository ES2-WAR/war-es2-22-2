import pygame
import pygame.gfxdraw

from Territory import Territory

PIECE_IMG = pygame.Surface((30,30), pygame.SRCALPHA)
COLORS = { 
  'branco': (255,255,255),
  'vermelho': (255,0,0),
  'verde': (0,255,0),
  'azul': (0,0,255),
  'preto': (0,0,0),
  'amarelo': (212, 175, 55)
}


class Piece(pygame.sprite.Sprite):
  def __init__(self, territoryColor: str, pos_x: int, pos_y: int, troops: int, territoryId: int, radius: int):
    super().__init__()
    self.selected = False
    self.color = territoryColor
    self.territoryId = territoryId
    self.pos_x = pos_x
    self.pos_y = pos_y
    self.troops = troops
    self.radius = radius
    self.frame = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
    pygame.draw.circle(self.frame, COLORS[self.color], (self.radius, self.radius), self.radius, 0)
    self.rect = self.frame.get_rect()
    self.rect.center = (pos_x, pos_y)
  
  def updatePiece(self, relatedTerritory: Territory):
    self.troops = relatedTerritory.numberOfTroops

    if self.selected:
      if relatedTerritory.color == 'preto':
        pygame.draw.circle(self.frame, COLORS['branco'], (self.radius, self.radius), self.radius, 0)
      else:
        pygame.draw.circle(self.frame, COLORS['preto'], (self.radius, self.radius), self.radius, 0) 
    else: 
      pygame.draw.circle(self.frame, COLORS[relatedTerritory.color], (self.radius, self.radius), self.radius, 0)