from functools import *

class Territory():
  def __init__(self, color: str, neighbours: list[int]):
    self.color = color
    self.neighbours = neighbours
    self.numberOfTroops = 10
    self.region = 'blank'
