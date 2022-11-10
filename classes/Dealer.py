from classes.Territory import *
from classes.Region import *
from classes.Card import *
from random import randrange


class Dealer():
  JOKERCARDS = 2
  MIN_ARMY_FROM_TERRITORIES_POSSESSED = 3
  CARD_QUANTITY_OF_ARMY_RECEIVED_PER_TRADE = [4, 6, 8, 10, 12, 15] #...20, 25, 30, 35, 40...
    
  def __init__(self, playersInGame: int, initialTerritoryList: list[Territory], regionList: list[Region]):
    self.players = playersInGame
    self.initialTerritoryList = initialTerritoryList
    self.regionList = regionList
    self.startingTerritories = []
    self.numberOfTrades = 0

  # retorna a instancia da carta sorteada para o jogador
  # tem chance de virar joker
  def getCardAfterSuccessfullAttack(self) -> Card:
      lenTerritoriesList = len(self.initialTerritoryList)
      territoryId = randrange(0, lenTerritoriesList + self.JOKERCARDS)
      return Card(territoryId, territoryId >= lenTerritoriesList)
      
  # retorna a lista de territorios iniciais por id de jogador
  def listOfStartingTerritoriesOfAllPlayers(self) -> list[list[int]]:
      usersTerritories = [[] for p in range(self.players)]
      allTerritoriesId = list(map(lambda t : t.id, self.initialTerritoryList))
      # Arbitrario, pode vir como parametro
      nextPlayerToReceiveTerritory = 0 
      while allTerritoriesId:
          randomListPosition = randrange(0, len(allTerritoriesId))
          usersTerritories[nextPlayerToReceiveTerritory].append(allTerritoriesId[randomListPosition])
          allTerritoriesId.pop(randomListPosition)
          nextPlayerToReceiveTerritory = (nextPlayerToReceiveTerritory + 1) % self.players
      self.startingTerritories = usersTerritories
      return usersTerritories
  
  # retorna a lista de territorios iniciais do jogador
  def startingTerritoriesOfPlayer(self, playerId: int) -> list[int]:
      if not self.startingTerritories:
          self.listOfStartingTerritoriesOfAllPlayers()
      return self.startingTerritories[playerId]
  
  # retorna a quantidade de exercitos que deve ser colocado no tabuleiro antes do ataque
  # metade dos territorios conquistados 
  # minimo de exercitos a receber é sempre 3
  def receiveArmyFromPossessedTerritories(self, currentTerritoriesList: list[Territory]) -> int:
      return max(self.MIN_ARMY_FROM_TERRITORIES_POSSESSED, len(currentTerritoriesList) // 2)
  
  # retorna a quantidade de exercitos que deve ser colocado no tabuleiro antes do ataque
  # troca de cartas
  # jogador não pode ter mais de 5 cartas na mao
  def receiveArmyFromTradingCards(self, handOfCards: list[Card], doAllPossibleTrades: bool = False) -> int:
      bonusArmy = 0
      while self.hasCardsToTrade(handOfCards):
        tradeThreeCardsPerTroop()
        if self.numberOfTrades < len(self.CARD_QUANTITY_OF_ARMY_RECEIVED_PER_TRADE):
            bonusArmy += self.CARD_QUANTITY_OF_ARMY_RECEIVED_PER_TRADE[self.numberOfTrades]
        else:
            bonusArmy += (self.numberOfTrades - len(self.CARD_QUANTITY_OF_ARMY_RECEIVED_PER_TRADE) + 1) * 5 + self.CARD_QUANTITY_OF_ARMY_RECEIVED_PER_TRADE[-1]
        self.numberOfTrades += 1
        if not doAllPossibleTrades:
            break
      return bonusArmy
  
  def hasCardsToTrade(self, handOfCards: list[Card]) -> bool:
      listOfCardsShapes = list(map(lambda c : c.shape, handOfCards))
      # Com certeza tem combinação de cartas pra troca
      if len(handOfCards) >= 5:
          return True
      # Tem trocas de mesma forma
      if listOfCardsShapes.count('T') + listOfCardsShapes.count('J') >= 3 or listOfCardsShapes.count('S') + listOfCardsShapes.count('J') >= 3 or listOfCardsShapes.count('C') + listOfCardsShapes.count('J') >= 3:
          return True
      # Tem trocas de formas diferentes
      differentShapesInList = 0
      if 'T' in listOfCardsShapes:
          differentShapesInList += 1
      if 'S' in listOfCardsShapes:
          differentShapesInList += 1
      if 'C' in listOfCardsShapes:
          differentShapesInList += 1
      if 'J' in listOfCardsShapes:
          differentShapesInList += 1
      return differentShapesInList >= 3
  
  # retorna a quantidade de exercitos que deve ser colocado no tabuleiro antes do ataque
  # bonus de regiao conquistada
  # exercitos de bonus de regiao so devem ser colocados na regiao
  def receiveArmyFromPossessedRegions(self):
      pass