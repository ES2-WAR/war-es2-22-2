from Territory import *
from Region import *
from Card import *
from random import randint


class Dealer():
  JOKERCARDS = 2
    
  def __init__(self, playersInGame: int, territoryList: list[Territory], regionList: list[Region]):
    self.players = playersInGame

  # retorna a instancia da carta sorteada para o jogador
  # tem chance de virar joker
  def getCardAfterSuccessfullAttack(self) -> Card:
      territoryId = randint(0, len(territoryId) + self.JOKERCARDS)
      return Card(territoryId, territoryId >= len(territoryId))
      
  
  # retorna a lista de territorios iniciais por id de jogador
  def listOfStartingTerritoriesOfAllPlayers(self):
      pass
  
  # retorna a lista de territorios iniciais do jogador
  def startingTerritoriesOfPlayer(self):
      pass
  
  # retorna a quantidade de exercitos que deve ser colocado no tabuleiro antes do ataque
  # metade dos territorios conquistados 
  # minimo de exercitos a receber é sempre 3
  def receiveArmyFromPossessedTerritories(self):
      pass
  
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