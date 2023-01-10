#importing required libraries
import random

def deck_generator(deck_description:dict):
  final_deck = []
  for key in deck_description:
    final_deck = [*final_deck, *[key] * deck_description[key]]
  return final_deck


def deck_shuffler(deck: list):
  deck_limit = len(deck)
  li=range(1,deck_limit + 1)
  order = random.sample(li,deck_limit)
  shuffled_deck = []

  for i in order:
    shuffled_deck = [*shuffled_deck, deck[i - 1]]
  
  return shuffled_deck

