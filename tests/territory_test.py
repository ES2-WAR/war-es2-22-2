from classes.GameMap import *
from classes.Territory import *

def test_neighbourhoods():
  testTerritories: list[Territory] = [Territory('0', [1, 2]), Territory('0', [0, 4]), Territory('1', [0, 3]), Territory('1', [2, 4, 5] ), Territory('0', [3, 1]), Territory('1', [3])]
  testMap = GameMap(testTerritories)
  
  assert testMap.getFriendlyTerritoryNeighbours(3) == [2, 5]
  assert testMap.getHostileTerritoryNeighbours(0) == [2]
  assert testMap.getHostileTerritoryNeighbours(5) == []
  assert testMap.getTerritoryNeighbours(3) == [2, 4, 5]
