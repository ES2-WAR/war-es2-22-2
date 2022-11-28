import pygame_gui
import pygame

class GameUI:
  def __init__(self, manager: pygame_gui.UIManager):
    self.blitzButton = pygame_gui.elements.UIButton(
      relative_rect=pygame.Rect((0, -160), (100, 50)),
      text='Blitz',
      manager=manager,
      anchors={
        'centerx': 'centerx',
        'bottom': 'bottom'
      }
    )
    self.blitzButton.hide()
    self.blitzButton.disable()
    self.selectableTroops = pygame_gui.elements.UISelectionList(
      relative_rect=pygame.Rect((0, -100), (200, 70)),
      item_list=['1', '2', '3', '4', '5'], manager=manager,
      anchors={
        'centerx': 'centerx',
        'bottom': 'bottom'
      }
    )
    self.selectableTroops.hide()
    self.selectableTroops.disable()

    self.phase = 'Inactive'
  
  def addItemsToSelectableTroops(self, soldierRange: list[str]):
    self.selectableTroops.add_items(soldierRange)

  def setPhase(self, phase: str):    
    if phase == 'Inactive':
      self.selectableTroops.remove_items(list(map(lambda x: x['text'], self.selectableTroops.item_list)))
      self.selectableTroops.hide()
      self.selectableTroops.disable()
      if self.blitzButton.is_enabled:
        self.blitzButton.hide()
        self.blitzButton.disable()
    elif phase == 'Attack':
      self.blitzButton.show()
      self.blitzButton.enable()
      self.selectableTroops.show()
      self.selectableTroops.enable()
    self.phase = phase
  
  def getSelectedOptionFromList(self):
    selection = list(filter(lambda item: item['selected'], self.selectableTroops.item_list))
    if len(selection) == 0: return None
    return int(selection[0].text)