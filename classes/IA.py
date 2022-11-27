from GameMap import *
from Territory import *
from Game import *
from Player import *




class IA(Player):     # herda da classe player
    def __init__(self):
        pass

    def get_territories(self, idterritory: int):
        for territory in self.territories:
            if territory.id == idterritory:
                return territory.getDefendingTroops()

    def sort_territories_by_bsr_ascendant(self):
        self.territories.sort(key= lambda x: x.bsr)

    def sort_territories_by_bsr_descendant(self):
        self.territories.sort(key= lambda x: x.bsr, reverse=True)
    
    def set_border_countries(self):
        self.borderCountries = filter(lambda x: x.bst != 0, self.territories)

       
    def initiation_attack(self):
        self.set_border_countries()
        originCountries: list[Territory]
        for country in self.borderCountries:
            if country.bsr < 0.9:
                originCountries.append(country)
        self.main_attack(originCountries)
    
    def main_attack(self, originCountries: list[Territory]):
        while originCountries:
            country = originCountries.pop(0)
            targetCountries = sorted(GameMap.getHostileTerritoryNeighbours(country.id), key= lambda x: x.numberOfTroops)
            for target in targetCountries:
                targetTroops = target.numberOfTroops # soh fiz isso pra comparacao com as perdas depois
                if targetTroops >= country.numberOfTroops:
                    break
                losses = GameMap.attackEnemyTerritoryBlitz(country.id, target.id)
                if losses[1] == targetTroops:
                    self.borderCountries.append(target)


    def supply(self, additionalTroops: int):    # objetivo é deixar a distribuicao de tropas nos territorios a mais equilibrada possivel
        self.set_border_countries()
        while additionalTroops > 0:
            targetCountries = sorted(self.borderCountries, key= lambda country: country.bsr, reverse=True) # ordenar pelos bsr mais altos
            if targetCountries[0].gainTroops(1):
                additionalTroops = additionalTroops -1

    def move(self):
        innerCountries =  filter(lambda x: x.bst == 0, self.territories)
        originCountries = filter(lambda country: country.numberOfTroops > 1, innerCountries)
        
        while originCountries:
            origin = originCountries.pop(0)
            targetCountries = sorted(self.set_border_countries(), key= lambda country: country.bsr, reverse=True)
            for target in targetCountries:
                path = GameMap.moveTroopsBetweenFriendlyTerrirories(origin.id, target.id, 100)
                if path != []:
                    break

                    
                        