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
  
  def canMoveTroopsBetweenTerriroriesAux(self, fromTerritoryId: int, toTerritoryId: int, visitedTerritoriesId:list[int], currentPath: list[int]) -> Tuple[bool, list[int]]:
    if fromTerritoryId == toTerritoryId:
      return True, currentPath + [fromTerritoryId]
    if fromTerritoryId in visitedTerritoriesId:
      return False, []
    currentPath += [fromTerritoryId]
    visitedTerritoriesId.append(fromTerritoryId)
    listOfPossiblePaths = list(map(lambda t: self.canMoveTroopsBetweenTerriroriesAux(t, toTerritoryId, visitedTerritoriesId, currentPath), self.getFriendlyTerritoryNeighbours(fromTerritoryId)))
    for possiblePath in listOfPossiblePaths:
      if possiblePath[0]:
        return True, possiblePath[1]
    return False, []
  
  def moveTroopsBetweenTerrirories(self, fromTerritoryId: int, toTerritoryId: int, numberOfTroops: int) -> list[int]:
    possiblePathToDestiny = self.canMoveTroopsBetweenTerriroriesAux(fromTerritoryId, toTerritoryId, [], [])
    if not possiblePathToDestiny[1]:
      return []
    troopsLost = self.territories[fromTerritoryId].loseTroops(numberOfTroops)
    self.territories[toTerritoryId].gainTroops(troopsLost)
    return possiblePathToDestiny[1]
    
  