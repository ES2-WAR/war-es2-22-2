from classes.GameMap import *
from classes.Territory import *
from classes.Region import *

testTerritories: list[Territory] = [Territory('0', [1, 2], 0, 'teste1', 0), Territory('0', [0, 4], 0, 'teste2', 1), Territory('1', [0, 3], 0, 'teste3', 2), Territory('1', [2, 4, 5], 1, 'teste4', 3), Territory('0', [3, 1], 1, 'teste5', 4), Territory('1', [3], 0, 'teste6', 5), Territory('0', [7], 2, 'teste6', 6), Territory('0', [6], 2, 'teste7', 7)]
testRegions: list[Region] = [Region('a', 3, 0), Region('b', 2, 1), Region('c', 2, 2)]
testMap = GameMap(testTerritories, testRegions)

def test_neighbourhoods():
  
  assert testMap.getFriendlyTerritoryNeighbours(3) == [2, 5]
  assert testMap.getHostileTerritoryNeighbours(0) == [2]
  assert testMap.getHostileTerritoryNeighbours(5) == []
  assert testMap.getTerritoryNeighbours(3) == [2, 4, 5]

def test_regions():
  
  assert testMap.filterTerritoriesByRegion(1) == [3, 4]
  assert testMap.filterTerritoriesByRegion(0) == [0, 1, 2, 5]
  assert testMap.filterTerritoriesByRegion(2) == [6, 7]
  assert testMap.filterTerritoriesByRegion(3) == []

def test_troopsMovement():
  testMap.moveTroopsBetweenTerrirories(0, 1, 5)
  assert testTerritories[0].numberOfTroops == 5
  assert testTerritories[1].numberOfTroops == 15
  testMap.moveTroopsBetweenTerrirories(0, 1, 5)
  assert testTerritories[0].numberOfTroops == 1
  assert testTerritories[1].numberOfTroops == 19
  testMap.moveTroopsBetweenTerrirories(2, 1, 2)
  assert testTerritories[0].numberOfTroops == 1
  assert testTerritories[2].numberOfTroops == 10
  testMap.moveTroopsBetweenTerrirories(2, 5, 2)
  assert testTerritories[2].numberOfTroops == 8
  assert testTerritories[5].numberOfTroops == 12