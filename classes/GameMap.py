from classes.Territory import *
from functools import *

class GameMap():
  def __init__(self, territoryList: list[Territory]):
    self.territories: list[Territory] = territoryList
  
  def getTerritoryNeighbours(self, index: int) -> list[int]:
    return self.territories[index].neighbours
  
  def getFriendlyTerritoryNeighbours(self, index: int) -> list[int]:
    return list(filter(lambda x: self.territories[x].color == self.territories[index].color, self.territories[index].neighbours))
  
  def getHostileTerritoryNeighbours(self, index: int) -> list[int]:
    return list(filter(lambda x: self.territories[x].color != self.territories[index].color, self.territories[index].neighbours))
