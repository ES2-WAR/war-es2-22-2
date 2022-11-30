class Player():
  def __init__(self, playerId: int, playerName: str, color: str, isAI: bool = False):
    self.id = playerId
    self.color = color
    self.name = playerName
    self.isAI = isAI
    
  def get_territories(self, game):
      player_territories = []
      for territory in game.territories:
          if territory.color == self.color:
              player_territories.append(territory)
      return player_territories
