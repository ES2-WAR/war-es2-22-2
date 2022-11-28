from GameMap import *
from Territory import *
from Game import *
from Player import *




class IA(Player):     # herda da classe player
    def __init__(self):
        pass
    
    def set_border_countries(self):
        self.borderCountries = filter(lambda x: x.bst != 0, self.territories)

    def sort_bsr_ascendant(self):
        return filter(lambda y: y.bsr < 0.5, sorted(filter(lambda x: x.numberOfTroops > 1, self.terrotories), key=lambda country: country.bsr))

    def sort_bsr_descendant(self):
        return filter(lambda y: y.bsr > 1, sorted(self.terrotories, key=lambda country: country.bsr, reverse=True))
       
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
                path = GameMap.moveTroopsBetweenFriendlyTerrirories(origin.id, target.id, 100)      # ideia é mandar todas as tropas para o territorio que mais precisa
                if path != []:
                    break


        # fazer a parte de movimentacao das tropas de territorios com bsr baixo para territorios com bsr alto
        originCountries = self.sort_bsr_ascendant()
        targetCountries = self.sort_bsr_descendant()

        while originCountries:
            origin = originCountries.pop(0)
            for target in targetCountries:
                path = GameMap.moveTroopsBetweenFriendlyTerrirories(origin.id, target.id, 1)
                if origin.bsr > 0.5: # movimentacao 'prejudicou' a origem, deve retornar a tropa
                    GameMap.moveTroopsBetweenFriendlyTerrirories(target.id, origin.id, 1)
                    break
