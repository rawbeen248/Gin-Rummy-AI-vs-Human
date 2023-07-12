# Importing necessary modules and classes
import sys
import random
from deck import Deck
from player import Player, Bot
from hand import Hand
from best_melds import identify_melds, find_best_meld, find_possible_deadwood

# Main class for the Gin Rummy game
class GinRummy:
    # Initialize the game
    def __init__(self):
        # Create and shuffle a new deck, create a player and a bot, and an empty discard pile
        self.deck = Deck()
        self.deck.shuffle()
        self.player = Player()
        self.bot = Bot(self)
        self.discard_pile = []

        # Deal initial hands to the player and the bot
        self.deal_initial_hands()

        # Initialize scores
        self.player_score = 0
        self.bot_score = 0

        # Initialize flags for game state
        self.player_knocked = False 
        self.game_ended = False

    # Set the bot for the game
    def set_bot(self, bot):
        self.bot = bot

    # Get the value of a card
    def card_value(self, card):
        # Dictionary to hold card values
        face_card_values = {
            'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
            '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13
        }
        return face_card_values.get(card.rank, 0)

    # Deal the initial hands to players
    def deal_initial_hands(self):
        # Create and shuffle a new deck
        self.deck = Deck()
        self.deck.shuffle()

        # Deal 10 cards to each player
        for _ in range(10):
            self.player.hand.add_card(self.deck.deal_card())
            self.bot.hand.add_card(self.deck.deal_card())

    # Identify the optimal melds for a hand
    def identify_optimal_melds(self, hand):
        # Find all possible melds
        possible_melds = identify_melds(hand.cards)

        # Find the best meld and the deadwood for the given melds
        best_melds, _ = find_best_meld(possible_melds, hand.cards)

        return best_melds

    # Calculate the deadwood for a hand
    def calculate_deadwood(self, hand):
        # Find the optimal melds
        melds = self.identify_optimal_melds(hand)

        # Get all cards that are in the melds
        melded_cards = [card for meld in melds for card in meld]

        # Calculate the points for the deadwood cards
        points = 0
        for card in hand.cards:
            if card not in melded_cards:
                points += self.card_value(card)

        return points

    # Check if a hand is a gin (i.e., has no deadwood)
    def is_gin(self, hand):
        return self.calculate_deadwood(hand) == 0

    # Check if a hand is valid to knock
    def is_valid_knock(self, hand):
        return self.calculate_deadwood(hand) <= 10

    # Process layoff for a hand
    def layoff(self, knocker_hand, opponent_hand):
        # Check the melds 
        knocker_melds = self.identify_optimal_melds(knocker_hand)
        opponent_melds = self.identify_optimal_melds(opponent_hand)

        opponent_deadwood_cards = [card for card in opponent_hand.cards if card not in [c for meld in opponent_melds for c in meld]]

        layoff_cards = []

        knocker_run_melds = [meld for meld in knocker_melds if meld[0].suit == meld[1].suit]

        # Check if any card of the opponent deadwood can be laid off on knocker's melds
        for meld in knocker_run_melds:
            meld.sort(key=lambda card: Deck.ranks.index(card.rank))
            lowest_card = meld[0]
            highest_card = meld[-1]

            for card in opponent_deadwood_cards:
                if card.suit == lowest_card.suit and Deck.ranks.index(card.rank) == Deck.ranks.index(lowest_card.rank) - 1 and card not in layoff_cards:
                    layoff_cards.append(card)
                elif card.suit == highest_card.suit and Deck.ranks.index(card.rank) == Deck.ranks.index(highest_card.rank) + 1 and card not in layoff_cards:
                    layoff_cards.append(card)

        knocker_set_melds = [meld for meld in knocker_melds if meld[0].rank == meld[1].rank]

        for meld in knocker_set_melds:

            for card in opponent_deadwood_cards:
                if card.rank == meld[0].rank and card not in layoff_cards:
                    layoff_cards.append(card)

        return layoff_cards


    # Calculate score for a round
    def calculate_score(self, knocker, opponent):

        if self.bot == knocker:
            layoff_cards = self.layoff(knocker.hand, opponent.hand)
        else:
            layoff_cards = self.layoff(opponent.hand, knocker.hand)

        print(f"Layoff cards: {layoff_cards}") 

        knocker_deadwood = self.calculate_deadwood(knocker.hand)
        print(f"Knocker deadwood: {knocker_deadwood}") 

        opponent_deadwood = self.calculate_deadwood(opponent.hand) - sum(self.card_value(card) for card in layoff_cards)
        print(f"Opponent deadwood: {opponent_deadwood}") 

        return knocker_deadwood, opponent_deadwood


    # Check if the game is over
    def is_game_over(self):
        # Game is over if player has gin, bot has gin, player knocked, or bot knocked
        if self.is_gin(self.player.hand) or self.is_gin(self.bot.hand) or self.player_knocked or self.is_valid_knock(self.bot.hand):
            self.game_ended = True
           

    # Handle the end of the game, calculate the scores and display the result
    def handle_end_game(self):
        print(f"\nGame ended!")

        print(f"Bot's hand: {self.bot.hand}")

        knocker, opponent = (self.player, self.bot) if self.player_knocked else (self.bot, self.player)

        knocker_deadwood, opponent_deadwood = self.calculate_score(knocker, opponent)

        print(f"Knocker Deadwood: {knocker_deadwood}, Opponent Deadwood: {opponent_deadwood}")

        if self.is_gin(knocker.hand):
            knocker.score += 25 + opponent_deadwood
        elif self.is_valid_knock(knocker.hand) and knocker_deadwood < opponent_deadwood:
            knocker.score += opponent_deadwood - knocker_deadwood
        elif self.is_valid_knock(knocker.hand) and knocker_deadwood >= opponent_deadwood:
            opponent.score += knocker_deadwood - opponent_deadwood + 15

        print(f"Round scores: Player: {self.player.score}, Bot: {self.bot.score}")

        if self.player.score == self.bot.score:
            print("It's a tie!")
        elif self.player.score > self.bot.score:
            print("Player is winning!")
        else:
            print("Bot is winning!")


    # Main game loop
    def play(self):
        """
        Main game loop that initiates and runs the Gin Rummy game until a player reaches 100 points.
        """

        while self.player.score < 100 and self.bot.score < 100:
            # Initialize the game variables for a new round.
            self.game_ended = False
            self.player_knocked = False
            self.deck = Deck()
            self.deck.shuffle()
            self.player.hand = Hand()
            self.bot.hand = Hand()
            self.discard_pile = []
            self.deal_initial_hands()

            # Loop for each round of the game.
            while not self.game_ended:                
                for current_player in [self.player, self.bot]:

                    is_player_turn = current_player == self.player

                    # If it's the player's turn
                    if is_player_turn:
                        # Prompt player to draw a card until a valid action is taken
                        while True:
                            melds = identify_melds(self.player.hand.cards)
                            chosen_melds, non_meld_cards  = find_best_meld(melds, self.player.hand.cards)
                            possible_deadwood, complete_deadwood = find_possible_deadwood(non_meld_cards)
                            print(f'\nYour hand: {self.player.hand}')
                            print("\nMelds Chosen: ",chosen_melds)
                            print("\nPossible Deadwood:  ",possible_deadwood)
                            print("\nComplete Deadwood: ",complete_deadwood)
                            print(f'\nDiscard pile: {self.discard_pile}')
                            print("\n---Draw a card---")
                            print("\nEnter 'p' to pick from the discard pile, 'd' to draw from the deck: ")
                            choice = input().strip().lower()
                            sys.stdin.flush() 
                            
                            # Player decides to pick from the discard pile
                            if choice == 'p':
                                if not self.discard_pile:
                                    print("\nDiscard pile is empty! Try picking from the deck('d').")
                                    continue
                                self.player.hand.add_card(self.discard_pile.pop())
                                break

                            # Player decides to draw from the deck
                            elif choice == 'd':
                                if not self.deck.cards:
                                    print("\nDeck is empty! Reshuffling discarded pile into the deck.")
                                    self.deck.cards.extend(self.discard_pile)
                                    self.deck.shuffle()
                                    self.discard_pile.clear()
                                self.player.hand.add_card(self.deck.deal_card())
                                break

                            # Player input is not recognized
                            else:
                                print("\nInvalid input! Please try again.")
                                continue

                        print(f'\nYour hand after drawing: {self.player.hand}')

                    else: # If it's the bot's turn
                        self.bot.update_deadwood_sum()
                        self.bot.choose_card_to_pick(self.discard_pile, self.deck)

                    # If game has ended, break from the loop
                    if self.game_ended:
                        break

                    # If it's the player's turn
                    if is_player_turn:
                        melds = identify_melds(self.player.hand.cards)
                        chosen_melds, non_meld_cards  = find_best_meld(melds, self.player.hand.cards)
                        possible_deadwood, complete_deadwood = find_possible_deadwood(non_meld_cards)
                        print("\nMelds Chosen: ",chosen_melds)
                        print("\nPossible Deadwood:  ",possible_deadwood)
                        print("\nComplete Deadwood: ",complete_deadwood)
                                        
                        continue_turn = True 
                        while continue_turn:
                            print("\n---Discard a card---")
                            print("\nEnter the card to discard (e.g., 'QH' for Queen of Hearts), 'k' to knock, 'g' to gin: ")
                            choice = input().strip().upper()

                            if choice == 'K' or choice == 'G':
                                print(f"\nChoose a card to discard before {'knocking' if choice == 'K' else 'declaring gin'} (e.g., 'QH' for Queen of Hearts):")
                                discard_choice = input().strip().upper()

                                card_to_discard = None
                                for card in self.player.hand.cards:
                                    if f'{card.rank}{card.suit}' == discard_choice:
                                        card_to_discard = card
                                        break

                                if card_to_discard:
                                    self.player.hand.discard_card(card_to_discard)
                                    self.discard_pile.append(card_to_discard)
                                    
                                    if choice == 'K' and self.is_valid_knock(self.player.hand):
                                        print("\nYou made a valid knock!")
                                        self.player_knocked = True
                                        self.game_ended = True
                                        continue_turn = False 
                                        break

                                    elif choice == 'G' and self.is_gin(self.player.hand):
                                        print("\nYou have Gin!")
                                        self.player_knocked = True
                                        self.game_ended = True
                                        continue_turn = False
                                        break

                                    else:
                                        print("\nInvalid action! Not a valid knock or gin.")
                                        self.player.hand.add_card(self.discard_pile.pop())
                                else:
                                    print("\nInvalid card. Please enter a valid card from your hand.")

                            else:

                                card_to_discard = None
                                for card in self.player.hand.cards:
                                    if f'{card.rank}{card.suit}' == choice:
                                        card_to_discard = card
                                        break

                                if card_to_discard:
                                    self.player.hand.discard_card(card_to_discard)
                                    self.discard_pile.append(card_to_discard)
                                    continue_turn = False 
                                else:
                                    print("\nInvalid card. Please enter a valid card from your hand.")

                        print(f'\nDiscard pile: {self.discard_pile}')

                    else: # If it's the bot's turn
                        bot_action, card_to_discard = self.bot.choose_card_to_discard()
                        print(f'\nBot decided to {bot_action} and discarded: {card_to_discard.rank}{card_to_discard.suit}')
                        self.bot.hand.discard_card(card_to_discard)
                        self.discard_pile.append(card_to_discard)

                        if bot_action == "knock" and self.is_valid_knock(self.bot.hand):
                            print("\nBot made a valid knock!")
                            self.bot_knocked = True
                            self.game_ended = True
                        elif bot_action == "gin" and self.is_gin(self.bot.hand):
                            print("\nBot has Gin!")
                            self.bot_knocked = True
                            self.game_ended = True

                        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

                # Call handle_end_game if game has ended
                if self.game_ended:
                    self.handle_end_game()

