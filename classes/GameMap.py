from random import randint
from typing import Tuple
from classes.Territory import *
from classes.Region import *
from functools import *

class GameMap():
  def __init__(self, territoryList: list[Territory], regionList: list[Region]):
    self.territories = territoryList
    self.regions = regionList
    self.lastTerritoryAttackedAndAttacker = (-1, -1)
  
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
  
  def moveTroopsBetweenFriendlyTerrirories(self, fromTerritoryId: int, toTerritoryId: int, numberOfTroops: int) -> list[int]:
    possiblePathToDestiny = self.canMoveTroopsBetweenFriendlyTerriroriesAux(fromTerritoryId, toTerritoryId, [], [])
    if not possiblePathToDestiny[1]:
      return []
    troopsLost = self.territories[fromTerritoryId].deallocateTroops(numberOfTroops)
    self.territories[toTerritoryId].gainTroops(troopsLost)
    return possiblePathToDestiny[1]
  
  def moveDifferentNumberOfTroopsToColonyAfterAttack(self, colonyTerritoryId: int, newNumberOfTroopsInColony: int):
    if self.lastTerritoryAttackedAndAttacker[0] != colonyTerritoryId:
      return
    numberOfTroopsOverDesired = self.territories[colonyTerritoryId].numberOfTroops - newNumberOfTroopsInColony
    self.moveTroopsBetweenFriendlyTerrirories(colonyTerritoryId, self.lastTerritoryAttackedAndAttacker[1], numberOfTroopsOverDesired)
  
  def rollDices(self, numberOfDices: int) -> list[int]:
    MAX_OF_DICES_PER_ATTACK = 3
    finalNumberOfDices = min(numberOfDices, MAX_OF_DICES_PER_ATTACK)
    return list(randint(1, 6) for i in range(finalNumberOfDices))
  
  def colonize(self, colonizerTerritoryId: int, colonyTerritoryId: int):
    self.territories[colonyTerritoryId].colonize(self.territories[colonizerTerritoryId].color)
    self.lastTerritoryAttackedAndAttacker = (colonyTerritoryId, colonizerTerritoryId)
    self.moveTroopsBetweenFriendlyTerrirories(colonizerTerritoryId, colonyTerritoryId, self.territories[colonizerTerritoryId].getNonDefendingTroops())
    
  def getSuccessfullAttacks(self, numberOfAttackerTroops: int, numberOfDefenderTroops: int) -> Tuple[int, int]:
    attackersDiceResult = self.rollDices(numberOfAttackerTroops)
    defendersDiceResult = self.rollDices(numberOfDefenderTroops)
    defendersDiceResult.sort(reverse=True)
    attackersDiceResult.sort(reverse=True)
    battlesWonByAttackers = 0
    battlesWonByDefenders = 0
    for i in range(len(attackersDiceResult) if len(attackersDiceResult) < len(defendersDiceResult) else len(defendersDiceResult)):
      if attackersDiceResult[i] > defendersDiceResult[i]:
        battlesWonByAttackers += 1
      else:
        battlesWonByDefenders
    return battlesWonByAttackers, battlesWonByDefenders
  
  def attackEnemyTerritory(self, attackerTerritoryId: int, defenderTerritoryId: int) -> Tuple[int, int]:
    if defenderTerritoryId not in self.getHostileTerritoryNeighbours(attackerTerritoryId):
      return 0, 0
    numberOfTroopsAttacking = self.territories[attackerTerritoryId].getNonDefendingTroops()
    numberOfDefendingTroops = self.territories[defenderTerritoryId].getDefendingTroops()
    battlesWonByAttackersAndDefenders = self.getSuccessfullAttacks(numberOfTroopsAttacking, numberOfDefendingTroops)
    troopsLostByAttacker = self.territories[attackerTerritoryId].loseTroops(battlesWonByAttackersAndDefenders[1])
    troopsLostByDefender = self.territories[defenderTerritoryId].loseTroops(battlesWonByAttackersAndDefenders[0])
    if self.territories[defenderTerritoryId].hasAliveTroops():
      return troopsLostByAttacker, troopsLostByDefender
    self.colonize(attackerTerritoryId, defenderTerritoryId)
    return troopsLostByAttacker, troopsLostByDefender
    
  