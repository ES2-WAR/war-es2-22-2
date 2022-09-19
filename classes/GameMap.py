from codecs import unicode_escape_decode
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
  
  def __canMoveTroopsBetweenTerriroriesAux(self, fromRegionId: int, toRegionId: int, visitedTerritoriesId:list[int]) -> bool:
    if fromRegionId == toRegionId:
      return True
    if fromRegionId in visitedTerritoriesId:
      return False
    visitedTerritoriesId.append(fromRegionId)
    return any(map(lambda t: self.__canMoveTroopsBetweenTerriroriesAux(t, toRegionId, visitedTerritoriesId), self.getFriendlyTerritoryNeighbours(fromRegionId)))
  
  def moveTroopsBetweenTerrirories(self, fromRegionId: int, toRegionId: int, numberOfTroops: int):
    if not self.__canMoveTroopsBetweenTerriroriesAux(fromRegionId, toRegionId, []):
      return 
    troopsLost = self.territories[fromRegionId].loseTroops(numberOfTroops)
    self.territories[toRegionId].gainTroops(troopsLost)
    
  