from Territory import *
from Region import *

class Player():
    def __init__(self, color: str, territories: list[Territory], regions_conquered: list[Region], name: str):
        self.color = color
        self.terrotories = territories
        self.regions_conquered = regions_conquered
        self.name = name
        