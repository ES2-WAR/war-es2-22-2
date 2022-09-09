from classes.GameMap import *
from classes.Territory import *
from classes.Region import *

testTerritories: list[Territory] = [Territory('0', [1, 2], 'a', 'teste1', 0), Territory('0', [0, 4], 'a', 'teste2', 1), Territory('1', [0, 3], 'a', 'teste3', 2), Territory('1', [2, 4, 5], 'b', 'teste4', 3), Territory('0', [3, 1], 'b', 'teste5', 4), Territory('1', [3], 'a', 'teste6', 5)]
testRegions: list[Region] = [Region('a', 3, 0), Region('b', 2, 1)]
testMap = GameMap(testTerritories, testRegions)

def test_neighbourhoods():
  
  assert testMap.getFriendlyTerritoryNeighbours(3) == [2, 5]
  assert testMap.getHostileTerritoryNeighbours(0) == [2]
  assert testMap.getHostileTerritoryNeighbours(5) == []
  assert testMap.getTerritoryNeighbours(3) == [2, 4, 5]

def test_regions():
  
  assert testMap.filterTerritoriesByRegion('b') == [3, 4]
  assert testMap.filterTerritoriesByRegion('a') == [0, 1, 2, 5]
