import itertools
from deck import Deck

# Function to identify all possible melds from a hand
def identify_melds(hand):
    melds = [] # List to store all melds
    suits_cards = {'H': [], 'D': [], 'C': [], 'S': []}
    
    # Categorize cards based on their suit
    for card in hand:
        suits_cards[card.suit].append(card)

    # Identify and store melds based on sequential cards of same suit
    for suit, cards in suits_cards.items():
        cards.sort(key=lambda card: Deck.ranks.index(card.rank)) # Sort cards by their rank
        
        # Find consecutive cards of same suit
        for i in range(len(cards)):
            for j in range(i + 3, len(cards) + 1):
                run = cards[i:j]
                if all(Deck.ranks.index(run[k].rank) == Deck.ranks.index(run[k - 1].rank) + 1 for k in range(1, len(run))):
                    melds.append(run) # If a run (sequential cards of same suit) is found, add it to the melds

    # Dictionary to group cards by their rank
    rank_cards = {}
    for card in hand:
        rank_cards.setdefault(card.rank, []).append(card)

    # Identify and store melds based on cards of same rank
    for cards in rank_cards.values():
        if len(cards) >= 3: # If 3 or more cards of same rank found, add to the melds
            melds.append(cards) 
            if len(cards) == 4: # If 4 cards of same rank found, add all possible combinations of 3 cards to the melds
                for combo in itertools.combinations(cards, 3):
                    melds.append(list(combo))

    return melds # Return all possible melds



# Function to filter out the best melds, i.e., the melds that do not overlap with the checked meld
def best_melds(melds, check_meld):
    cleanmelds = []  # Store the melds that are "clean" i.e., don't overlap with check_meld

    # Check each meld
    for meld in melds:
        clean = True  # Assume the meld is clean

        # Check each card in meld against each card in check_meld
        for cardA in meld:
            for cardB in check_meld:
                # If card from meld is in check_meld, mark meld as not clean
                if cardA == cardB:
                    clean = False

        # If the meld is clean, add it to the list of clean melds
        if clean:
            count = 0
            # Ensure that the meld isn't already in cleanmelds
            for i in range(len(meld)):
                if meld[i] not in (item for sublist in cleanmelds for item in sublist):
                    count += 1
                    if count == len(meld):
                        cleanmelds.append(meld)

    # Add the check_meld to the list of clean melds and return the list
    cleanmelds.append(check_meld)
    return cleanmelds



# Get the numeric value of a card
def card_value(card):
    # Define values for face cards
    face_card_values = {
        'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13
    }
    # Return the value for the card rank
    return face_card_values.get(card.rank, 0)



# Calculate the sum of card values in a meld
def calculate_meld_sum(meld):
    # Use the card_value function on each card and sum up the values
    return sum(card_value(card) for card in flatten_list(meld))



# Flatten a nested list
def flatten_list(nested_list):
    # Loop through each sublist in the nested list and each item in the sublist
    return [val for sublist in nested_list for val in sublist]



# Check if a card is part of any melds
def is_card_in_melds(card, melds):
    # Flatten the list of melds and check if the card is in it
    flat_melds = flatten_list(melds)
    return any(card == item for item in flat_melds)



# Get the cards that are not part of the chosen melds
def get_non_meld_cards(hand, chosen_melds):
    if chosen_melds:
        # Flatten the list of chosen melds
        flat_chosen_melds = flatten_list(chosen_melds)
        # Return all cards that are not in the chosen melds
        return [card for card in hand if card not in flat_chosen_melds]
    else:
        # If there are no chosen melds, return the entire hand
        return [card for card in hand]



# Function to separate the deadwood cards into possible and complete deadwood
def find_possible_deadwood(rejected_cards):
    possible_deadwood = [] # Cards that has higher potential to form a meld in the future (like sets of 2 cards)
    complete_deadwood = [] # Cards that are confirmed to be deadwood
    
    rank_cards = {}
    for card in rejected_cards:
        rank_cards.setdefault(card.rank, []).append(card)
        
    for cards in rank_cards.values():
        if len(cards) == 2:
            possible_deadwood.extend(cards)
    
    suits_cards = {'H': [], 'D': [], 'C': [], 'S': []}
    for card in rejected_cards:
        suits_cards[card.suit].append(card)

    # Go through the rejected cards and sort them by suit
    for suit, cards in suits_cards.items():
         # Sort the cards by rank
        cards.sort(key=lambda card: Deck.ranks.index(card.rank))
        # Check for sequences in the sorted cards
        for i in range(len(cards) - 1):
            # If two cards are sequential, add them to the possible deadwood
            if Deck.ranks.index(cards[i + 1].rank) == Deck.ranks.index(cards[i].rank) + 1:
                possible_deadwood.extend([cards[i], cards[i + 1]])
    
    possible_deadwood = list(set(possible_deadwood))
    complete_deadwood = [card for card in rejected_cards if card not in possible_deadwood]
    
    # Return the possible and complete deadwood
    return possible_deadwood, complete_deadwood



# Choose the best melds out of all possible melds
def find_best_meld(melds, hand):
    final_chosen_melds = [] # List to store the chosen melds
    
    # If there are any possible melds
    if melds:
        # Find the best melds for each meld in the possible melds
        best_possible_melds = [best_melds(melds, check_meld) for check_meld in melds]
        # Calculate the sum of card values in each possible meld
        sum_of_possible_melds = [calculate_meld_sum(meld) for meld in best_possible_melds]

        if sum_of_possible_melds:
            index_of_highest_sum = sum_of_possible_melds.index(max(sum_of_possible_melds))
            final_chosen_melds.append(best_possible_melds[index_of_highest_sum])
            final_chosen_melds = flatten_list(final_chosen_melds)

        # Get the cards that are not part of the chosen melds
        rejected_cards = get_non_meld_cards(hand, final_chosen_melds)
        # Return the chosen melds and the rejected cards
        return final_chosen_melds, rejected_cards
    # If there are no possible melds, return an empty list and the entire hand
    return final_chosen_melds, hand