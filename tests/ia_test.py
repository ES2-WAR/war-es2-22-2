import re
from classes.GameMap import *
from classes.Territory import *
from classes.Region import *
from classes.IA import *




# PARA FAZER OS TESTES, TEM QUE COLOCAR O ATRIBUTO COLOR EM TERRITORIO
# ACREDITO QUE DEPOIS DE INTEGRADO, VAI OCORRER NORMALMENTE



testTerritories: list[Territory] = [Territory([1, 2], 0, 'teste0', 0, 10, 10, 'azul'), Territory([0, 4], 0, 'teste1', 1, 10, 10, 'azul'), Territory([0, 3, 4], 0, 'teste2', 2, 10, 10, 'branco'), Territory([2, 4, 5], 1, 'teste3', 3, 10, 10, 'branco'), Territory([3, 1, 2], 1, 'teste4', 4, 10, 10, 'azul'), Territory([3], 0, 'teste5', 5, 10, 10, 'branco'), Territory([7], 2, 'teste6', 6, 10, 10, 'azul'), Territory([6], 2, 'teste7', 7, 10, 10, 'azul')]
testRegions: list[Region] = [Region('a', 3, 0), Region('b', 2, 1), Region('c', 2, 2)]
testMap = GameMap(testTerritories, testRegions)
ia1= IA(testMap, 1, 'ia1', 'azul')
ia2= IA(testMap, 2, 'ia2', 'branco')



def test_ia_supply():
  print('SUPPLY')
  for territory in testTerritories:
      print(f'{territory.name} tem {territory.numberOfTroops} tropas\n')

  ia1.supply(5)

  for territory in testTerritories:
      print(f'{territory.name} tem {territory.numberOfTroops} tropas\n')


def test_ia_attack():

  print('ATTACK')
  print('===============================')

  ia1.initiation_attack()

  for territory in testTerritories:
      print(f'{territory.name} do IA {territory.color} tem {territory.numberOfTroops} tropas\n')

  print('===============================')



def test_ia_move():

  print('MOVE')
  print('===============================')

  ia1.move()

  for territory in testTerritories:
      print(f'{territory.name} do IA {territory.color} tem {territory.numberOfTroops} tropas\n')

  print('===============================')

test_ia_supply()
test_ia_attack()
test_ia_move()