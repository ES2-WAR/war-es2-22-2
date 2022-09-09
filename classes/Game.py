import pygame
from pygame.locals import *
 
class Game:
  def __init__(self):
    self._running = True
    self._display_surf = None
    self.size = self.weight, self.height = 800, 600

  def on_init(self):
    pygame.init()
    self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
    
    self.map: pygame.Surface = pygame.image.load("./assets/testMap.png")
    self.scaledMap = pygame.transform.smoothscale(self.map, (self.map.get_width() * (self.weight / self.map.get_width()), self.map.get_height() * (self.height / self.map.get_height())))
    self._running = True

  def on_event(self, event):
    if event.type == pygame.QUIT:
      self._running = False
  def on_loop(self):
    pass
  def on_render(self):
    self._display_surf.blit(self.scaledMap, self.scaledMap.get_rect())
    pygame.display.flip()
  def on_cleanup(self):
    pygame.quit()

  def on_execute(self):
    if self.on_init() == False:
      self._running = False

    while(self._running):
      for event in pygame.event.get():
        self.on_event(event)
      self.on_loop()
      self.on_render()
    self.on_cleanup()
 
if __name__ == "__main__" :
  theGame = Game()
  theGame.on_execute()