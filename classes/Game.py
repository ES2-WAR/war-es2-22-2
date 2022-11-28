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
from classes.GameUI import *
import pygame_gui


pygame.init()
FONT_SIZE = 15
NUMBER_OF_PLAYERS = 6
PLAYER_ID = 0
GAME_STAGES = ["DRAFT", "DEPLOY", "ATTACK", "FORTIFY"]

class Game:
  def __init__(self):
    self.running = True
    self.window = None
    
    # criacao dos jogadores
    self.players: list[Player] = []
    for p in range(NUMBER_OF_PLAYERS):
      self.players.append(Player(p, "Jogador "+  str(p+1), list(COLORS)[p], p != PLAYER_ID))

    # criacao dos territorio e regioes
    self.territories: list[Territory] = [Territory([1,3,29],0,'Alaska',0,99, 139),Territory([0,3,4,2],0,'Mackenzie',1,245, 127),Territory([1,5,13],0,'Groenlandia',2,422, 98),Territory([0,1,4,6],0,'Vancouver',3,187, 200),Territory([1,3,5,7],0,'Ottwa',4,285, 221),Territory([4,7,2],0,'Labrador',5,335, 219),Territory([3,7,8,4],0,'California',6,193, 285),Territory([4,5,6,8],0,'Nova York',7,285, 303),Territory([6,7,9],0,'Mexico',8,199, 362),Territory([8,10,11],1,'Colombia',9,278, 456),Territory([9,11,12],1,'Bolivia',10,316, 549),Territory([9,10,12,20],1,'Brasil',11,389, 535),Territory([10,11],1,'Argentina',12,317, 634),Territory([2,16,14],2,'Islandia',13,522, 182),Territory([16,15,13,17],2,'Suecia',14,600, 198),Territory([14,17,19,26,32,35],2,'Moscou',15,709, 242),Territory([13,17,18,14],2,'Inglaterra',16,500, 237),Territory([15,16,18,19,14],2,'Alemanha',17,602, 280),Territory([16,17,19,20,21],2,'Portugal',18,511, 378),Territory([17,18,21,35,15],2,'Polonia',19,631, 339),Territory([18,11,23,22,21],3,'Argelia',20,559, 499),Territory([18,20,22,35,19],3,'Egito',21,668, 452),Territory([21,20,23,25],3,'Sudão',22,707, 535),Territory([20,22,24],3,'Congo',23,654, 590),Territory([23,22,25],3,'Africa do Sul',24,667, 688),Territory([22,24],3,'Madagascar',25,760, 690),Territory([15,27,31,33,32],4,'Omsk',26,826, 214),Territory([26,28,30,31],4,'Dudinka',27,884, 145),Territory([27,30,29],4,'Siberia',28,970, 123),Territory([28,30,33,0],4,'Vladivostok',29,1060, 130),Territory([28,27,31,33,29],4,'Tchita',30,953, 219),Territory([30,27,26,33,34],4,'Mongolia',31,972, 291),Territory([26,15,35,36,33],4,'Aral',32,810, 305),Territory([31,26,32,36,37,34],4,'China',33,960, 359),Territory([29,31],4,'Japao',34,1079, 311),Territory([15,19,21,36,32],4,'Oriente Medio',35,735, 408),Territory([32,35,33,37,38],4,'India',36,878, 417),Territory([33,36,39],4,'Vietna',37,978, 455),Territory([36,41],5,'Sumatra',38,990, 574),Territory([37,40,41],5,'Nova Guiné',39,1099, 551),Territory([39,41],5,'Nova Zelândia',40,1138, 676),Territory([38,39,40],5,'Australia',41,1036, 691)]
    self.regions: list[Region] = [Region('América do Norte', 3, 0), Region('América do Sul', 2, 1), Region('Europa', 2, 2), Region('Africa', 9, 3), Region('Ásia', 6, 4), Region('Oceania', 2, 5)]
    self.dealer = Dealer(NUMBER_OF_PLAYERS, self.territories, self.regions)
    # distribui territorios entre os jogadores
    playersTerritories = self.dealer.listOfStartingTerritoriesOfAllPlayers()
    for playerInd in range(len(playersTerritories)):
      ownerColor = self.players[playerInd].color
      for territoryInd in playersTerritories[playerInd]:
        self.territories[territoryInd].colonize(ownerColor)
    self.gameMap = GameMap(self.territories, self.regions)
    # criacao da fonte para o texto da quantidade de tropas
    self.font = pygame.font.SysFont("Arial", FONT_SIZE)
    self.manager = pygame_gui.UIManager((1200, 800))
    self.clock = pygame.time.Clock()
    # self.gameUI.blitzButton = pygame_gui.elements.UIButton(
    #   relative_rect=pygame.Rect((0, -160), (100, 50)),
    #   text='Blitz',
    #   manager=self.manager,
    #   anchors={
    #     'centerx': 'centerx',
    #     'bottom': 'bottom'
    #   }
    # )
    self.gameUI = GameUI(self.manager)
    self.gameUI.setPhase('Attack')
    # self.gameUI.blitzButton.hide()
    # self.gameUI.blitzButton.disable()
    # self.gameUI.selectableTroops = pygame_gui.elements.UISelectionList(
    #   relative_rect=pygame.Rect((0, -100), (200, 70)),
    #   item_list=[], manager=self.manager,
    #   anchors={
    #     'centerx': 'centerx',
    #     'bottom': 'bottom'
    #   }
    # )
    # self.gameUI.selectableTroops.hide()
    # self.gameUI.selectableTroops.disable()

    # criacao do grupo de sprites e populando ele com novas peças baseadas nos territorios da territoryList
    self.pieces_group = pygame.sprite.Group()
    self.selected_pieces_group = pygame.sprite.Group()
    for territory in self.territories:
      new_piece = Piece(territory.color, territory.pos_x, territory.pos_y, territory.numberOfTroops, territory.id, 15)
      selected_piece = Piece(territory.color, territory.pos_x, territory.pos_y, territory.numberOfTroops, territory.id, 18)
      self.pieces_group.add(new_piece)
      self.selected_pieces_group.add(selected_piece)


  def onInit(self):
    pygame.init()
    self.window = Window(1200, 800)
    self.graphicalMap = GraphicalMap("classes/assets/tabuleiro_nomeado.png", self.window.width, self.window.height)
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
      if self.players[0].color != self.territories[pieceTerritoryId].color:
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
    
    if event.type == pygame_gui.UI_BUTTON_PRESSED:
      if not self.gameUI.blitzButton.hovered:
        print("Lista pressionada")
        print("Lista: {}".format(str(self.gameUI.selectableTroops.item_list)))
      #botão da seleção apertado
      else:
        print("botao")
        # self.gameUI.selectableTroops.add_items(['banana'])
        # self.gameUI.selectableTroops.remove_items(list(map(lambda x: x['text'], self.gameUI.selectableTroops.item_list)))

    if event.type == pygame.MOUSEBUTTONDOWN: # botão é apertado
      print("mouse coordinates (x, y): {}, {}".format(mousePosition[0], mousePosition[1]))
      isPlayerTurn = self.playerRound == 0
      pieceClickedTerritorryId = -1
      for piece in pieces:
        if piece.rect.collidepoint(mousePosition[0], mousePosition[1]):
          pieceClickedTerritorryId = piece.territoryId
          break
        
      # se não for round dele, invalida
      if isPlayerTurn:
        self.handlePieceClick(pieceClickedTerritorryId)
        
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
    for selected_piece in self.selected_pieces_group:
      selected_piece.selected = False
      if selected_piece.territoryId in self.gameMap.selectedTerritories:
        selected_piece.selected = True
      selected_piece.updatePiece(self.gameMap.territories[selected_piece.territoryId])
      text = self.font.render(str(selected_piece.troops), True, (150,150,150))
      self.graphicalMap.image.blit(selected_piece.frame, selected_piece.rect)
    for piece in self.pieces_group:
      piece.selected = False
      piece.updatePiece(self.gameMap.territories[piece.territoryId])
      text = self.font.render(str(piece.troops), True, (150,150,150))
      self.graphicalMap.image.blit(piece.frame, piece.rect)
      self.graphicalMap.image.blit(text, (piece.rect[0] + FONT_SIZE/2, piece.rect[1] + FONT_SIZE/2))
    pygame.display.flip()
    self.manager.draw_ui(self.graphicalMap.image)

  def onCleanup(self):
    pygame.quit()

  def onExecute(self):
    if self.onInit() == False:
      self.running = False

    while(self.running):
      timeDelta = self.clock.tick(60)/1000.0
      for event in pygame.event.get():
        self.onEvent(event)
        self.manager.process_events(event)
      self.manager.update(timeDelta)
      self.onLoop()
      self.onRender()

    self.onCleanup()
 
if __name__ == "__main__" :
  theGame = Game()
  theGame.onExecute()