from pickle import FALSE
from random import choice

class Card():
  def __init__(self, territoryId: int, isJoker: bool = False):
    if isJoker:
      self.turnIntoJoker()
      return
    typesOfCard = ['A', 'B', 'C']
    self.type = choice(typesOfCard)
    self.territoryId = territoryId
    
  def turnIntoJoker(self):
    self.type = 'J'
    self.territoryId = -1
