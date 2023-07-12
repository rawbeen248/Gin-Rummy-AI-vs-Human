from deck import Deck

class Hand:
    # Initialize the hand with no cards
    def __init__(self):
        self.cards = []

    # Add a card to the hand
    def add_card(self, card):
        self.cards.append(card)

    # Remove a card from the hand
    def discard_card(self, card):
        self.cards.remove(card)

    # Sort the cards in the hand by suit and rank
    def sort(self):
        self.cards.sort(key=lambda card: (Deck.suits.index(card.suit), Deck.ranks.index(card.rank)))
    
    # Define an iterator for the hand
    def __iter__(self):
        return iter(self.cards)
    
    # Define a representation for the hand
    def __repr__(self):
        self.sort()
        return str(self.cards)
