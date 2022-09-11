import pygame

class Window:
  def __init__(self, width, height):
    self.displaySize = self.width, self.height = width, height
    self.display = pygame.display.set_mode(self.displaySize, pygame.HWSURFACE | pygame.DOUBLEBUF)
