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
    testTerritories: list[Territory] = [Territory('branco',[1,3,29],0,'Alaska',0,93, 124),Territory('branco',[0,3,4,2],0,'Mackenzie',1,194, 124),Territory('vermelho',[1,5,13],0,'Groenlandia',2,422, 81),Territory('branco',[0,1,4,6],0,'Vancouver',3,187, 188),Territory('branco',[1,3,5,7],0,'Ottwa',4,267, 201),Territory('branco',[4,7,2],0,'Labrador',5,342, 204),Territory('branco',[3,7,8,4],0,'California',6,187, 269),Territory('preto',[4,5,6,8],0,'Nova York',7,280, 291),Territory('branco',[6,7,9],0,'Mexico',8,199, 362),Territory('branco',[8,10,11],1,'Colombia',9,284, 433),Territory('vermelho',[9,11,12],1,'Chile',10,295, 531),Territory('branco',[9,10,12,20],1,'Brasil',11,377, 515),Territory('branco',[10,11],1,'Argentina',12,305, 627),Territory('branco',[2,16],2,'Islandia',13,519, 162),Territory('preto',[16,15],2,'Suecia',14,615, 147),Territory('branco',[14,17,19,26,32,35],2,'Moscou',15,713, 207),Territory('branco',[13,17,18,14],2,'Inglaterra',16,505, 255),Territory('branco',[15,16,18,19],2,'Alemanha',17,598, 263),Territory('preto',[16,17,19,20,21],2,'Portugal',18,528, 336),Territory('branco',[17,18,21,35,15],2,'Polonia',19,617, 332),Territory('branco',[18,11,23,22,21],3,'Argelia',20,549, 476),Territory('branco',[18,20,22,35,19],3,'Egito',21,645, 444),Territory('preto',[21,20,23,25],3,'Sudão',22,703, 530),Territory('branco',[20,22,24],3,'Congo',23,646, 576),Territory('branco',[23,22,25],3,'Africa do Sul',24,654, 674),Territory('verde',[22,24],3,'Madagascar',25,760, 679),Territory('branco',[15,27,31,33,32],4,'Omsk',26,821, 180),Territory('verde',[26,28,30,31],4,'Dudinka',27,882, 137),Territory('branco',[27,30,29],4,'Siberia',28,974, 109),Territory('branco',[28,30,33,0],4,'Vladivostok',29,1060, 111),Territory('branco',[28,27,31,33,29],4,'Tchita',30,955, 204),Territory('preto',[30,27,26,33],4,'Mongolia',31,970, 273),Territory('vermelho',[26,15,35,36,33],4,'Aral',32,803, 292),Territory('preto',[31,26,32,36,37,34],4,'China',33,937, 348),Territory('branco',[29,33],4,'Japao',34,1093, 284),Territory('branco',[15,19,21,36,32],4,'Oriente Medio',35,735, 408),Territory('branco',[32,35,33,37,38],4,'India',36,867, 403),Territory('verde',[33,36,39],4,'Vietna',37,961, 436),Territory('vermelho',[36,41],5,'Sumatra',38,981, 559),Territory('preto',[37,40,41],5,'Borneo',39,1084, 533),Territory('branco',[39,41],5,'Nova Guiné',40,1133, 661),Territory('vermelho',[38,39,40],5,'Australia',41,1028, 667)]
    testRegions: list[Region] = [Region('América do Norte', 3, 0), Region('América do Sul', 2, 1), Region('Europa', 2, 2), Region('Africa', 9, 3), Region('Ásia', 6, 4), Region('Oceania', 2, 5)]
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
          break
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