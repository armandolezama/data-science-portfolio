#importing required libraries
import random

class game_simulator:
  def __init__(self, deck_description) -> None:
    self.deck_description = {**deck_description}
    self.deck = self.deck_shuffler(self.deck_generator(deck_description))
    self.hand = []
  
  def draw(self, cards:int):
    self.hand = [*self.hand ,*self.deck[:cards]]
    self.deck = self.deck[cards:len(self.deck)]
    self.update_description()

  def update_description(self):
    for card in self.hand:
      self.deck_description[card] = self.deck_description[card] - 1

  def deck_generator(self, deck_description:dict):
    final_deck = []
    for key in deck_description:
      final_deck = [*final_deck, *[key] * deck_description[key]]
    return final_deck

  def deck_shuffler(self, deck:list):
    deck_limit = len(deck)
    li=range(1,deck_limit + 1)
    order = random.sample(li,deck_limit)
    shuffled_deck = []

    for i in order:
      shuffled_deck = [*shuffled_deck, deck[i - 1]]
    
    return shuffled_deck
