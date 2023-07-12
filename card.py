class Card:
    # Initialize the card with a rank and suit
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    # Define a representation for the card
    def __repr__(self):
        return f'{self.rank}{self.suit}'
