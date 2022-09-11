import pygame
from pygame.locals import *
from GraphicalMap import *
from Window import *
 
class Game:
  def __init__(self):
    self.running = True
    self.window = None

  def onInit(self):
    pygame.init()
    self.window = Window(800, 600)
    self.graphicalMap = GraphicalMap("./assets/testMap.png", self.window.width, self.window.height)
    self.running = True

  def onEvent(self, event):
    if event.type == pygame.QUIT:
      self.running = False

  def onLoop(self):
    pass

  def onRender(self):
    self.window.display.blit(self.graphicalMap.image, self.graphicalMap.image.get_rect())
    pygame.display.flip()

  def onCleanup(self):
    pygame.quit()

  def onExecute(self):
    if self.onInit() == False:
      self.running = False

    while(self.running):
      for event in pygame.event.get():
        self.onEvent(event)
      self.onLoop()
      self.onRender()
    self.onCleanup()
 
if __name__ == "__main__" :
  theGame = Game()
  theGame.onExecute()