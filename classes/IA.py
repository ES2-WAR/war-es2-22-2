from GameMap import *
from Territory import *
from Game import *
from Player import *




class IA(Player):     # herda da classe player
    def __init__(self, territoryList: list[Territory], regionList: list[Region]):
        self.mapTerritories = territoryList
        self.territories: list[Territory]
        self.regions = regionList


    def get_territories(self, idterritory: int):
        for territory in self.territories:
            if territory.id == idterritory:
                return territory.getDefendingTroops()

    def sort_territories_by_bsr_ascendant(self):
        self.territories.sort(key= lambda x: x.bsr)

    def sort_territories_by_bsr_descendant(self):
        self.territories.sort(key= lambda x: x.bsr, reverse=True)

    def attack(self):
        self.sort_territories_by_bsr_ascendant()
        for terriroty in self.territories:
            if terriroty.bsr >= 1:
                break
            else:
                hostile_neighbours = GameMap.getHostileTerritoryNeighbours(terriroty.id)
                hostile_neighbours.sort(key= lambda x: x.numberOfTroops)
                for hostile in hostile_neighbours:
                    if hostile.numberOfTroops >= terriroty.numberOfTroops:
                        break
                    else:
                        pass # ATTACK -> pensando em faazer uma funcao auxiliar que faz esse ataque, inves de copiar toda aquela logica aqui

    def supply(self, additionalTroops: int):
        while additionalTroops > 0:
            self.sort_territories_by_bsr_descendant()
            # SUPPLY NO PRIMEIRO TERRITORIO DA LISTA -> fazer a logica de supply 
            additionalTroops = additionalTroops - 1

    def move_troops(self):
        self.sort_territories_by_bsr_ascendant
        for i in range(len(self.territories)):
            if self.territories[i].numberOfTroops > 1:
                pass # MOVE ENTRE self.territories[i] e self.territories[-1-i]

            
                