from typing import Tuple
import pygame
from pygame.locals import *
from classes.GraphicalMap import *
from classes.Window import *
from classes.Piece import *
from classes.Territory import *
from classes.Region import *
from classes.GameMap import *
from classes.Dealer import *
from classes.Player import *

pygame.init()
FONT_SIZE = 12
NUMBER_OF_PLAYERS = 6
# 0: branco
# 1: vermelho
# 2: verde
# 3: azul
# 4: preto
# 5: amarelo
PLAYER_ID = 0
GAME_STAGES = ["DRAFT", "DEPLOY", "ATTACK", "FORTIFY"]

class Game:
  def __init__(self):
    pygame.init()
    self.window = Window(1024, 700)
    self.graphicalMap = GraphicalMap("classes/assets/images/bg/water.png", self.window.width, self.window.height)
    
    # criacao dos jogadores
    self.players: list[Player] = []
    for p in range(NUMBER_OF_PLAYERS):
      self.players.append(Player(p, "Jogador "+  str(p+1), list(COLORS)[p], p != PLAYER_ID))

    # criacao dos territorio e regioes
    self.territories: list[Territory] = [
      Territory([1,3,29],0,'Alaska',0,32,75,82,107),
      Territory([0,3,4,2],0,'Mackenzie',1,107,62,176,112),
      Territory([1,4,5,13],0,'Groelandia',2,285,25,358,73),
      Territory([0,1,4,6],0,'Vancouver',3,117,131,164,166),
      Territory([1,2,3,5,6,7],0,'Ottawa',4,198,134,225,179),
      Territory([4,7,2],0,'Labrador',5,260,129,299,177),
      Territory([3,7,8,4],0,'California',6,122,200,169,240),
      Territory([4,5,6,8],0,'NovaYork',7,179,200,238,259),
      Territory([6,7,9],0,'Mexico',8,131,278,178,327),
      Territory([8,10,11],1,'Colombia',9,203,359,245,387),
      Territory([9,11,12],1,'Bolivia',10,197,406,258,471),
      Territory([9,10,12,20],1,'Brasil',11,220,389,329,454),
      Territory([10,11],1,'Argentina',12,234,484,267,559),
      Territory([2,16,14],2,'Islandia',13,411,124,438,143),
      Territory([16,15,13,17],2,'Suecia',14,478,91,521,127),
      Territory([14,17,19,26,32,35],2,'Moscou',15,538,94,597,201),
      Territory([13,17,18,14],2,'Inglaterra',16,381,171,428,227),
      Territory([15,16,18,19,14],2,'Alemanha',17,467,185,516,235),
      Territory([16,17,19,20,21],2,'Portugal',18,404,250,445,300),
      Territory([17,18,21,35,15],2,'Polonia',19,475,249,527,291),
      Territory([18,11,23,22,21],3,'Argelia',20,417,344,481,422),
      Territory([18,20,22,35,19],3,'Egito',21,505,364,554,392),
      Territory([21,20,23,25],3,'Sudao',22,553,416,604,469),
      Territory([20,22,24],3,'Congo',23,503,457,554,508),
      Territory([23,22,25],3,'AfricadoSul',24,515,525,562,598),
      Territory([22,24],3,'Madagascar',25,625,534,654,578),
      Territory([15,27,31,33,32],4,'Omsk',26,668,69,700,170),
      Territory([26,28,30,31],4,'Dudinka',27,692,37,758,132),
      Territory([27,30,29],4,'Siberia',28,783,53,830,95),
      Territory([0,28,30,33,34],4,'Vladvostok',29,837,67,887,122),
      Territory([28,27,31,33,29],4,'Tchita',30,769,129,819,181),
      Territory([30,27,26,33,34],4,'Mongolia',31,775,186,830,242),
      Territory([26,15,35,36,33],4,'Aral',32,628,202,687,258),
      Territory([31,26,32,36,37,34],4,'China',33,722,222,807,305),
      Territory([29,31],4,'Japao',34,895,190,937,254),
      Territory([15,19,21,36,32],4,'OrienteMedio',35,550,302,628,366),
      Territory([32,35,33,37,38],4,'India',36,688,292,744,361),
      Territory([33,36,39],4,'Vietna',37,786,344,823,388),
      Territory([36,41],5,'Sumatra',38,782,454,840,498),
      Territory([37,40,41],5,'NovaGuine',39,881,444,930,473),
      Territory([39,41],5,'NovaZelandia',40,907,514,962,568),
      Territory([38,39,40],5,'Australia',41,840,530,881,595)]
    self.piecesColors = ["" for i in range(len(self.territories))]
    self.regions: list[Region] = [Region('América do Norte', 3, 0), Region('América do Sul', 2, 1), Region('Europa', 2, 2), Region('Africa', 9, 3), Region('Ásia', 6, 4), Region('Oceania', 2, 5)]
    self.dealer = Dealer(NUMBER_OF_PLAYERS, self.territories, self.regions)
    # distribui territorios entre os jogadores
    playersTerritories = self.dealer.listOfStartingTerritoriesOfAllPlayers()
    for playerInd in range(len(playersTerritories)):
      ownerColor = self.players[playerInd].color
      for territoryInd in playersTerritories[playerInd]:
        self.territories[territoryInd].colonize(ownerColor)
        self.piecesColors[territoryInd] = ownerColor
    self.gameMap = GameMap(self.territories, self.regions)
    # criacao da fonte para o texto da quantidade de tropas
    self.font = pygame.font.SysFont("arialblack", FONT_SIZE)

    # criacao do grupo de sprites e populando ele com novas peças baseadas nos territorios da territoryList
    self.pieces_group = pygame.sprite.Group()
    for territory in self.territories:
      new_piece = Piece(territory.id, territory.name, territory.color, territory.numberOfTroops, territory.pos_x, territory.pos_y, territory.text_x, territory.text_y)
      self.pieces_group.add(new_piece)


  def onInit(self):
    self.running = True
    self.gameStage = GAME_STAGES[0]
    self.playerRound = randint(0, NUMBER_OF_PLAYERS-1)
    self.troopsToDeploy = 0
    
  
  def goToNextStage(self):
    self.gameStage = GAME_STAGES[(GAME_STAGES.index(self.gameStage) + 1) % len(GAME_STAGES)]
    print(">> new stage is", self.gameStage)
    if GAME_STAGES.index(self.gameStage) == 0:
      self.goToNextPlayerRound()
    
    
  def goToNextPlayerRound(self):
    self.playerRound = (self.playerRound + 1) % NUMBER_OF_PLAYERS
    print(">> player turn:", self.players[self.playerRound].color)
  
    
  def handlePieceClick(self, pieceTerritoryId: int):
    if pieceTerritoryId == -1: #reset selected pieces
      self.gameMap.selectedTerritories = [-1, -1]
      return
    if self.gameMap.selectedTerritories[0] == -1 or pieceTerritoryId == self.gameMap.selectedTerritories[0]:
      if self.players[PLAYER_ID].color != self.territories[pieceTerritoryId].color:
        return
      self.gameMap.selectedTerritories[0] = pieceTerritoryId
    else:
      self.gameMap.selectedTerritories[1] = pieceTerritoryId
    
    if self.gameStage == "DEPLOY":
      deployingTroops = self.troopsToDeploy
      self.territories[pieceTerritoryId].gainTroops(deployingTroops)
      self.troopsToDeploy -= deployingTroops
      self.gameMap.selectedTerritories = [-1, -1]
      return
  
    if self.gameStage == "ATTACK" and -1 not in self.gameMap.selectedTerritories:
      losses = self.gameMap.attackEnemyTerritoryBlitz(self.gameMap.selectedTerritories[0], self.gameMap.selectedTerritories[1])
      print("losses:", losses)
      if not (losses[0] == losses[1] == 0): 
        self.gameMap.selectedTerritories = [-1, -1]
      else:
        self.gameMap.selectedTerritories[1] = -1
      return
        
    if self.gameStage == "FORTIFY" and -1 not in self.gameMap.selectedTerritories:
      path: list[int] = self.gameMap.moveTroopsBetweenFriendlyTerrirories(self.gameMap.selectedTerritories[0], self.gameMap.selectedTerritories[1], 10)
      if path == []:
        print(pieceTerritoryId, self.gameMap.selectedTerritories)
        self.gameMap.selectedTerritories[1] = -1
        print(pieceTerritoryId, self.gameMap.selectedTerritories)
      else:
        self.gameMap.selectedTerritories = [-1, -1]
        print(pieceTerritoryId, self.gameMap.selectedTerritories)
      return
    

  def onEvent(self, event):
    mousePosition: Tuple[int, int] = pygame.mouse.get_pos()
    pieces: list[Piece] = self.pieces_group.sprites()
    if event.type == pygame.QUIT:
      self.running = False
    
    if event.type == pygame.MOUSEBUTTONDOWN: # botão é apertado
      print("mouse coordinates (x, y): {}, {}".format(mousePosition[0], mousePosition[1]))
      isPlayerTurn = self.playerRound == PLAYER_ID
      pieceClickedTerritorryId = -1
      for piece in pieces:
        if piece.rect.collidepoint(mousePosition[0], mousePosition[1]) and piece.mask.get_at((mousePosition[0] - piece.rect.x, mousePosition[1] - piece.rect.y)):
          print(">> clicked on", piece.color, "piece")
          pieceClickedTerritorryId = piece.territoryId
          break
        
      # se não for round dele, invalida
      if isPlayerTurn:
        self.handlePieceClick(pieceClickedTerritorryId)
        if pieceClickedTerritorryId != -1:
          # forca update do territorio clicado
          self.piecesColors[pieceClickedTerritorryId] = ""
        
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
          self.goToNextStage()
        
  def onLoop(self):
    if self.gameStage == "DRAFT":
      troopsToReceive = 0
      player = self.players[self.playerRound]
      troopsToReceive += self.dealer.receiveArmyFromPossessedTerritories(player, self.territories)
      troopsToReceive += self.dealer.receiveArmyFromPossessedRegions(player, self.territories)
      print(">>", player.color, "received", troopsToReceive, "troops")
      self.troopsToDeploy = troopsToReceive
      self.goToNextStage()
      
    if self.gameStage == "DEPLOY" and self.troopsToDeploy <= 0:
      self.goToNextStage()

  def onRender(self):
    self.window.showMap(self.graphicalMap.image)
    for piece in self.pieces_group:
      wasSelected = piece.selected
      piece.selected = False
      if piece.territoryId in self.gameMap.selectedTerritories:
        piece.selected = True
      if self.piecesColors == piece.color and wasSelected == piece.selected:
        continue
      piece.updatePiece(self.gameMap.territories[piece.territoryId])
      text = self.font.render(str(piece.troops), True, (150,150,150))
      text_rect = text.get_rect(center=(piece.text_center_x, piece.text_center_y))
      pieceimg = piece.image.copy()
      if piece.selected:
        pieceimg.fill((10,10,10), special_flags=pygame.BLEND_RGB_SUB)
      self.graphicalMap.scaleAndBlit(pieceimg, piece.pos_x, piece.pos_y)
      self.graphicalMap.scaleAndBlit(text, text_rect.x, text_rect.y)
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