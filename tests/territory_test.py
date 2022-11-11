import re
from classes.GameMap import *
from classes.Territory import *
from classes.Region import *
from classes.Card import *
from classes.Dealer import *

testTerritories: list[Territory] = [Territory('0', [1, 2], 0, 'teste1', 0, 0, 0), Territory('0', [0, 4], 0, 'teste2', 1, 0, 0), Territory('1', [0, 3], 0, 'teste3', 2, 0, 0), Territory('1', [2, 4, 5], 1, 'teste4', 3, 0, 0), Territory('0', [3, 1], 1, 'teste5', 4, 0, 0), Territory('1', [3], 0, 'teste6', 5, 0, 0), Territory('0', [7], 2, 'teste6', 6, 0, 0), Territory('0', [6], 2, 'teste7', 7, 0, 0)]
testRegions: list[Region] = [Region('a', 3, 0), Region('b', 2, 1), Region('c', 2, 2)]
testMap = GameMap(testTerritories, testRegions)
nonJokerCard = Card()
jokerCard = Card(True)
dealer = Dealer(5, testTerritories, testRegions)

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
  assert testMap.moveTroopsBetweenFriendlyTerrirories(0, 1, 5) == [0, 1]
  assert testTerritories[0].numberOfTroops == 10
  assert testTerritories[1].numberOfTroops == 20
  assert testMap.moveTroopsBetweenFriendlyTerrirories(0, 1, 5) == [0, 1]
  assert testTerritories[0].numberOfTroops == 5
  assert testTerritories[1].numberOfTroops == 25
  assert testMap.moveTroopsBetweenFriendlyTerrirories(2, 1, 2) == []
  assert testTerritories[2].numberOfTroops == 15 
  assert testTerritories[1].numberOfTroops == 25
  assert testMap.moveTroopsBetweenFriendlyTerrirories(2, 5, 2) == [2, 3, 5]
  assert testTerritories[2].numberOfTroops == 13
  assert testTerritories[5].numberOfTroops == 17
  
def test_troopsManipulation():
  testTerritories[6].gainTroops(2)
  testTerritories[6].loseTroops(15)
  testTerritories[6].gainTroops(2)
  testTerritories[6].deallocateTroops(3)
  assert testTerritories[6].getDefendingTroops() == 1

def test_diceRolls():
  assert len(testMap.rollDices(5)) == 3
  assert len(testMap.rollDices(2)) == 2
  
def test_colony():
  testMap.colonize(3, 4)
  assert testMap.getFriendlyTerritoryNeighbours(3) == [2, 4, 5]
  
def test_attacking():
  attackerDices = [5, 6, 6]
  defenderDices = [3, 6, 5]
  battlesWonByAttackersAndDefenders = testMap.getSuccessfullAttacks(attackerDices, defenderDices)
  assert battlesWonByAttackersAndDefenders[0] == 2
  assert battlesWonByAttackersAndDefenders[1] == 1

def test_card_creation():
  assert nonJokerCard.shape in ['T', 'S', 'C']
  assert jokerCard.shape == "J"
  
def test_dealing():
  territoriesPerPlayer = dealer.listOfStartingTerritoriesOfAllPlayers()
  assert len(testTerritories) == len(sum(territoriesPerPlayer, []))
  