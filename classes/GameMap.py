from typing import Tuple
from classes.Territory import *
from classes.Region import *
from functools import *

class GameMap():
  def __init__(self, territoryList: list[Territory], regionList: list[Region]):
    self.territories = territoryList
    self.regions = regionList
  
  def getTerritoryNeighbours(self, index: int) -> list[int]:
    return self.territories[index].neighbours
  
  def getFriendlyTerritoryNeighbours(self, index: int) -> list[int]:
    return list(filter(lambda x: self.territories[x].color == self.territories[index].color, self.territories[index].neighbours))
  
  def getHostileTerritoryNeighbours(self, index: int) -> list[int]:
    return list(filter(lambda x: self.territories[x].color != self.territories[index].color, self.territories[index].neighbours))

  def filterTerritoriesByRegion(self, regionId: int) -> list[int]:
    return list(map(lambda y: y.id, filter(lambda x: x.regionId == regionId, self.territories)))
  
  def canMoveTroopsBetweenFriendlyTerriroriesAux(self, fromTerritoryId: int, toTerritoryId: int, visitedTerritoriesId:list[int], currentPath: list[int]) -> Tuple[bool, list[int]]:
    if fromTerritoryId == toTerritoryId:
      return True, currentPath + [fromTerritoryId]
    if fromTerritoryId in visitedTerritoriesId:
      return False, []
    currentPath += [fromTerritoryId]
    visitedTerritoriesId.append(fromTerritoryId)
    listOfPossiblePaths = list(map(lambda t: self.canMoveTroopsBetweenFriendlyTerriroriesAux(t, toTerritoryId, visitedTerritoriesId, currentPath), self.getFriendlyTerritoryNeighbours(fromTerritoryId)))
    for possiblePath in listOfPossiblePaths:
      if possiblePath[0]:
        return True, possiblePath[1]
    return False, []
  
  def moveTroopsBetweenTerrirories(self, fromTerritoryId: int, toTerritoryId: int, numberOfTroops: int) -> list[int]:
    possiblePathToDestiny = self.canMoveTroopsBetweenFriendlyTerriroriesAux(fromTerritoryId, toTerritoryId, [], [])
    if not possiblePathToDestiny[1]:
      return []
    troopsLost = self.territories[fromTerritoryId].deallocateTroops(numberOfTroops)
    self.territories[toTerritoryId].gainTroops(troopsLost)
    return possiblePathToDestiny[1]
  
  def getSuccessfullAttacks(self, numberOfAttackerTroops: int, numberOfDefenderTroops: int) -> Tuple[int, int]:
    MAX_OF_DICES_PER_ATTACK = 3
    attackersDiceResult = self.rollDices(min(numberOfAttackerTroops, MAX_OF_DICES_PER_ATTACK)).sort(reverse=True)
    defendersDiceResult = self.rollDices(min(numberOfDefenderTroops, MAX_OF_DICES_PER_ATTACK)).sort(reverse=True)
    battlesWonByAttackers = 0
    battlesWonByDefenders = 0
    for i in range(len(attackersDiceResult) if len(attackersDiceResult) < len(defendersDiceResult) else len(defendersDiceResult)):
      if attackersDiceResult[i] > defendersDiceResult[i]:
        battlesWonByAttackers += 1
      else:
        battlesWonByDefenders
    return battlesWonByAttackers, battlesWonByDefenders
  
  def rollDices(self, numberOfDices: int) -> list[int]:
    pass
  
  def colonize(self, colonizerTerritoryId: int, colonyTerritoryId: int):
    self.colonize(colonizerTerritoryId, colonyTerritoryId, self.territories[colonizerTerritoryId].getNonDefendingTroops())
    
  def colonize(self, colonizerTerritoryId: int, colonyTerritoryId: int, numberOfColonizerTroops: int):
    self.territories[colonyTerritoryId].colonize(self.territories[colonizerTerritoryId].color)
    self.moveTroopsBetweenTerrirories(colonizerTerritoryId, colonyTerritoryId, min(numberOfColonizerTroops, self.territories[colonizerTerritoryId].getNonDefendingTroops()))
    
  def attackEnemyTerritory(self, attackerTerritoryId: int, defenderTerritoryId: int):
    self.attackEnemyTerritory(attackerTerritoryId, defenderTerritoryId, self.territories[attackerTerritoryId].getNonDefendingTroops())
  
  def attackEnemyTerritory(self, attackerTerritoryId: int, defenderTerritoryId: int, numberOfTroopsAttacking: int):
    if defenderTerritoryId not in self.getHostileTerritoryNeighbours(attackerTerritoryId):
      return
    numberOfDefendingTroops = self.territories[defenderTerritoryId].getDefendingTroops()
    battlesWonByAttackersAndDefenders = self.getSuccessfullAttacks(numberOfTroopsAttacking, numberOfDefendingTroops)
    troopsLostByAttacker = self.territories[attackerTerritoryId].loseTroops(battlesWonByAttackersAndDefenders[1])
    troopsLostByDefender = self.territories[defenderTerritoryId].loseTroops(battlesWonByAttackersAndDefenders[0])
    if (self.territories[defenderTerritoryId].hasAliveTroops):
      return
    
    
  