from pickle import FALSE
from random import choice

class Card():
  def __init__(self, isJoker: bool = False):
    if isJoker:
      self.turnIntoJoker()
      return
    typesOfCard = ['A', 'B', 'C']
    self.type = choice(typesOfCard)
    
  def turnIntoJoker(self):
    self.type = 'J'
