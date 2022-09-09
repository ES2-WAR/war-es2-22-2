from functools import *

class Territory():
  def __init__(self, color: str, neighbours: list[int], regionId: int, territoryName: str, territoryId: int):
    self.id = territoryId
    self.color = color
    self.neighbours = neighbours
    self.numberOfTroops = 10
    self.regionId = regionId
    self.name = territoryName
