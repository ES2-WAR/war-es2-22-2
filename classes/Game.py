from typing import Tuple
import pygame
from pygame.locals import *
from GraphicalMap import *
from Window import *
from Piece import *
from Territory import *
from Region import *
from GameMap import *

pygame.init()
FONT_SIZE = 15

class Game:
  def __init__(self):
    self.running = True
    self.window = None

    # criacao dos dados teste de territorio e regioes
    testTerritories: list[Territory] = [Territory('branco', [1, 2], 0, 'Brasil', 0, 395, 523), Territory('vermelho', [0, 4], 0, 'Argentina', 1, 305, 617), Territory('preto', [0, 3], 0, 'Inglaterra', 2, 499, 252), Territory('vermelho', [2, 4], 1, 'China', 3, 950, 353), Territory('verde', [3, 1], 1, 'Moscou', 4, 706, 231)]
    testRegions: list[Region] = [Region('a', 3, 0), Region('b', 2, 1), Region('c', 2, 2)]
    self.gameMap = GameMap(testTerritories, testRegions)
    self.gameMap.territories[1].loseTroops(2)
    self.gameMap.territories[0].loseTroops(12)
    # criacao da fonte para o texto da quantidade de tropas
    self.font = pygame.font.SysFont("Arial", FONT_SIZE)

    # criacao do grupo de sprites e populando ele com novas peças baseadas nos territorios da territoryList
    self.pieces_group = pygame.sprite.Group()
    for territory in testTerritories:
      new_piece = Piece(territory.color, territory.pos_x, territory.pos_y, territory.numberOfTroops, territory.id)
      self.pieces_group.add(new_piece)


  def onInit(self):
    pygame.init()
    self.window = Window(1200, 800)
    self.graphicalMap = GraphicalMap("classes/assets/tabuleiro.png", self.window.width, self.window.height)
    self.running = True
    

  def onEvent(self, event):
    mousePosition: Tuple[int, int] = pygame.mouse.get_pos()
    pieces: list[Piece] = self.pieces_group.sprites()
    if event.type == pygame.QUIT:
      self.running = False
    if event.type == pygame.MOUSEBUTTONDOWN: #botão é apertado
      isPieceClick = False
      for piece in pieces:
        if piece.rect.collidepoint(mousePosition[0], mousePosition[1]):
          isPieceClick = True
          if self.gameMap.selectedTerritories[0] == -1:
            self.gameMap.selectedTerritories[0] = piece.territoryId
          elif piece.territoryId != self.gameMap.selectedTerritories[0]: 
            self.gameMap.selectedTerritories[1] = piece.territoryId
            if self.gameMap.territories[self.gameMap.selectedTerritories[0]].color == self.gameMap.territories[self.gameMap.selectedTerritories[1]].color:
              path: list[int] = self.gameMap.moveTroopsBetweenFriendlyTerrirories(self.gameMap.selectedTerritories[0], self.gameMap.selectedTerritories[1], 10)
              if path == []: self.gameMap.selectedTerritories[1] = -1
              else: self.gameMap.selectedTerritories = [-1, -1]
            else:
              losses = self.gameMap.attackEnemyTerritoryBlitz(self.gameMap.selectedTerritories[0], self.gameMap.selectedTerritories[1])
              if not (losses[0] == losses[1] == 0): self.gameMap.selectedTerritories = [-1, -1]
          else: self.gameMap.selectedTerritories = [-1, -1]
      print("mouse coordinates (x, y): {}, {}".format(mousePosition[0], mousePosition[1]))
      if not isPieceClick: self.gameMap.selectedTerritories = [-1, -1]
    # a ideia é fazer a lógica de clique dps que o overlay dos territórios estiver pronto
  def onLoop(self):
    pass

  def onRender(self):
    self.window.showMap(self.graphicalMap.image)
    for piece in self.pieces_group:
      piece.updatePiece(self.gameMap.territories[piece.territoryId])
      text = self.font.render(str(piece.troops), True, (150,150,150))
      self.graphicalMap.image.blit(piece.frame, piece.rect)
      self.graphicalMap.image.blit(text, (piece.rect[0] + FONT_SIZE/2, piece.rect[1] + FONT_SIZE/2))
    pygame.display.flip()

  def onCleanup(self):
    pygame.quit()

  def onExecute(self):
    if self.onInit() == False:
      self.running = False

    while(self.running):
      for event in pygame.event.get():
        self.onEvent(event)
      self.onLoop()
      self.onRender()
    self.onCleanup()
 
if __name__ == "__main__" :
  theGame = Game()
  theGame.onExecute()