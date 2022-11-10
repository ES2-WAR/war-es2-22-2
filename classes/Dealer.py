from classes.Territory import *
from classes.Region import *
from classes.Card import *
from random import randrange


class Dealer():
  JOKERCARDS = 2
  MIN_ARMY_FROM_TERRITORIES_POSSESSED = 3
    
  def __init__(self, playersInGame: int, initialTerritoryList: list[Territory], regionList: list[Region]):
    self.players = playersInGame
    self.initialTerritoryList = initialTerritoryList
    self.quantityOfTerritories = len(self.initialTerritoryList)
    self.regionList = regionList
    self.startingTerritories = []

  # retorna a instancia da carta sorteada para o jogador
  # tem chance de virar joker
  def getCardAfterSuccessfullAttack(self) -> Card:
      territoryId = randrange(0, self.quantityOfTerritories + self.JOKERCARDS)
      return Card(territoryId, territoryId >= self.quantityOfTerritories)
      
  # retorna a lista de territorios iniciais por id de jogador
  def listOfStartingTerritoriesOfAllPlayers(self) -> list[list[int]]:
      usersTerritories = [[] for p in range(self.players)]
      allTerritoriesId = list(map(lambda t : t.id, self.territoryList))
      # Arbitrario, pode vir como parametro
      nextPlayerToReceiveTerritory = 0 
      while allTerritoriesId:
          randomListPosition = randrange(0, self.quantityOfTerritories)
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
  # para cada territorio trocado que o jogador possuir, recebe extra 2 tropas para esse territorio
  # jogador não pode ter mais de 5 cartas na mao
  def receiveArmyFromTradingCards(self):
      pass
  
  # retorna a quantidade de exercitos que deve ser colocado no tabuleiro antes do ataque
  # bonus de regiao conquistada
  # exercitos de bonus de regiao so devem ser colocados na regiao
  def receiveArmyFromPossessedRegions(self):
      pass