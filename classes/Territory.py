from functools import *

class Territory():
  def __init__(self, color: str, neighbours: list[int], regionId: int, territoryName: str, territoryId: int):
    self.id = territoryId
    self.color = color
    self.neighbours = neighbours
    self.numberOfTroops = 10
    self.regionId = regionId
    self.name = territoryName
    
  def gainTroops(self, troops: int) -> bool:
    if troops <= 0:
      return False
    self.numberOfTroops += troops
    return True
    
  def loseTroops(self, troops: int) -> int:
    if troops <= 0:
      return 0
    remainingTroops = max(self.numberOfTroops - troops, 1)
    troopsLost = self.numberOfTroops - remainingTroops
    self.numberOfTroops = remainingTroops
    return troopsLost
