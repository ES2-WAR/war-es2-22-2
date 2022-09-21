from typing import Tuple
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
    self.graphicalMap = GraphicalMap("./assets/tabuleiro.png", self.window.width, self.window.height)
    self.running = True

  def onEvent(self, event):
    mousePosition: Tuple[int, int] = pygame.mouse.get_pos()
    if event.type == pygame.QUIT:
      self.running = False
    if event.type == pygame.MOUSEBUTTONDOWN: #botão é apertado
      print("mouse down")
      print("mouse coordinates (x, y): {}, {}".format(mousePosition[0], mousePosition[1]))
    if event.type == pygame.MOUSEBUTTONUP: #botão é solto
      print("mouse up")
      print("mouse coordinates (x, y): {}, {}".format(mousePosition[0], mousePosition[1]))
    
    # a ideia é fazer a lógica de clique dps que o overlay dos territórios estiver pronto
  def onLoop(self):
    pass

  def onRender(self):
    self.window.showMap(self.graphicalMap.image)
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