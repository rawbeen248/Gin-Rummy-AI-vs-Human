import random
from hand import Hand
from best_melds import identify_melds, find_best_meld, card_value, find_possible_deadwood

# Define a player class
class Player:
    def __init__(self):
        self.hand = Hand()  # Player's hand
        self.score = 0  # Player's score


# Define a bot class that inherits from player
class Bot(Player):

    def __init__(self, gin_rummy_instance):
        super().__init__()  # Call the parent class's initializer
        self.gin_rummy = gin_rummy_instance  # Instance of the game
        self.current_deadwood_sum = self.calculate_deadwood_sum()  # Current sum of deadwood


    # Method to calculate sum of deadwood
    def calculate_deadwood_sum(self):
        melds = identify_melds(self.hand.cards)
        chosen_melds, non_meld_cards  = find_best_meld(melds, self.hand.cards)
        possible_deadwood, complete_deadwood = find_possible_deadwood(non_meld_cards)
        return sum(card_value(card) for card in possible_deadwood + complete_deadwood)
    

    # Method to update sum of deadwood
    def update_deadwood_sum(self):
        self.current_deadwood_sum = self.calculate_deadwood_sum()


    # Method to choose a card to pick from the deck or discard pile
    def choose_card_to_pick(self, discard_pile, deck):
        # If there are cards in the discard pile, bot checks if the top card can improve its hand
        if discard_pile:
            top_discard = discard_pile[-1]
            self.hand.add_card(top_discard)

            melds = identify_melds(self.hand.cards)
            chosen_melds, non_meld_cards  = find_best_meld(melds, self.hand.cards)
            possible_deadwood, complete_deadwood = find_possible_deadwood(non_meld_cards)
            new_deadwood_sum = sum(card_value(card) for card in possible_deadwood + complete_deadwood)

            if new_deadwood_sum < self.current_deadwood_sum:  # If the new deadwood sum is less than current, bot keeps the card
                self.current_deadwood_sum = new_deadwood_sum
                discard_pile.pop()
                return
            else:
                self.hand.discard_card(top_discard)  # If not, bot discards the card

        # If deck is empty, reshuffle the discard pile into the deck
        if not deck.cards:
            print("Deck is empty! Reshuffling discarded pile into the deck.")
            deck.cards.extend(discard_pile)
            deck.shuffle()
            discard_pile.clear()

        self.hand.add_card(deck.deal_card())
        self.hand.sort()  # Sort the bot's hand


    # Method to choose a card to discard
    def choose_card_to_discard(self):
        melds = identify_melds(self.hand.cards)
        chosen_melds, non_meld_cards  = find_best_meld(melds, self.hand.cards)
        possible_deadwood, complete_deadwood = find_possible_deadwood(non_meld_cards)

        all_deadwood = complete_deadwood + possible_deadwood  # Sum of all deadwood
        all_deadwood.sort(key=card_value)

        # If there is no deadwood, bot considers to declare "gin"
        if len(all_deadwood) == 0:
            for meld in chosen_melds:
                if len(meld) > 3:
                    if all(card.rank == meld[0].rank for card in meld):
                        return ("gin", random.choice(meld))
                    else:
                        return ("gin", max(meld, key=card_value))

        # If there is only one deadwood, bot considers to declare "gin"
        if len(all_deadwood) == 1:
            return ("gin", all_deadwood[0])

        total_deadwood_score = sum(card_value(card) for card in all_deadwood[:-1])

        # If total score of deadwood is less than or equal to 10, bot considers to "knock"
        if total_deadwood_score <= 10:
            return ("knock", all_deadwood[-1])

        # If there is complete deadwood, bot discards the card with highest value
        if complete_deadwood:
            return ("discard", max(complete_deadwood, key=card_value))

        # If no complete deadwood, bot discards the card from possible deadwood with highest value
        return ("discard", max(possible_deadwood, key=card_value))
