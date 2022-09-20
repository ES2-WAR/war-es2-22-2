from functools import *

class Territory():
  def __init__(self, color: str, neighbours: list[int], regionId: int, territoryName: str, territoryId: int):
    self.id = territoryId
    self.color = color
    self.neighbours = neighbours
    self.numberOfTroops = 10
    self.regionId = regionId
    self.name = territoryName
    
  def getNonDefendingTroops(self) -> int:
    return self.numberOfTroops - 1
  
  def getDefendingTroops(self) -> int:
    return self.numberOfTroops
  
  def canAttack(self) -> bool:
    return self.getNonDefendingTroops() > 0
  
  def hasAliveTroops(self) -> bool:
    return self.numberOfTroops > 0
  
  def colonize(self, colonizerColor: str):
    self.color = colonizerColor
  
  def gainTroops(self, troops: int) -> bool:
    if troops <= 0:
      return False
    self.numberOfTroops += troops
    return True
  
  def loseTroops(self, troops: int) -> int:
    if troops <= 0:
      return 0
    remainingTroops = max(self.numberOfTroops - troops, 0)
    troopsLost = self.numberOfTroops - remainingTroops
    self.numberOfTroops = remainingTroops
    return troopsLost
    
  def deallocateTroops(self, troops: int) -> int:
    return self.loseTroops(min(self.getNonDefendingTroops(), troops))
    