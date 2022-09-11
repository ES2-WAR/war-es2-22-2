import pygame

class GraphicalMap:
  def __init__(self, mapImageLocation: str, windowWidth: int, windowHeight: int):
    unscaledMap: pygame.Surface = pygame.image.load(mapImageLocation)
    self.image: pygame.Surface = pygame.transform.smoothscale(unscaledMap, (unscaledMap.get_width() * (windowWidth / unscaledMap.get_width()), unscaledMap.get_height() * (windowHeight / unscaledMap.get_height())))

  def scaleToWindow(self, windowWidth: int, windowHeight: int):
    self.image = pygame.transform.smoothscale(self.image, (self.image.get_width() * (windowWidth / self.image.get_width()), self.image.get_height() * (windowHeight / self.image.get_height())))
  