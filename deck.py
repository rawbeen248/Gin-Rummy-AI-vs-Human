import random
from card import Card

class Deck:
    ranks = 'A 2 3 4 5 6 7 8 9 10 J Q K'.split()
    suits = 'H D C S'.split()

    def __init__(self):
        # Initialize the deck with a standard 52-card set
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    # Shuffle the deck
    def shuffle(self):
        random.shuffle(self.cards)

    # Deal the top card from the deck
    def deal_card(self):
        return self.cards.pop()
