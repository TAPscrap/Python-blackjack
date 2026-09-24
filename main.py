import random

from deck_lookup import deck

#------------------------------------------------------------------------------
# This program is a vitural blackjack simulater that has a artifial dealer.
# It is multi-player all the way up to 25 players but can crash at those numbers
# the program is most stable from 1 - 5 players and is generally stable up to 19.
#------------------------------------------------------------------------------

# draws a card from a list of cards notated by "current_deck"
def draw_card(current_deck):
    card = random.choice(current_deck)
    current_deck.remove(card)
    card_val = card[:-1] # removes the suit of the card for raw value

    # Find the value of the card if it is an ace it's alternate 1 value is avalulated later
    if card_val in ["J", "Q", "K"]:
        val = 10
    elif card_val == "A":
        val = 11
    else:
        val = int(card_val)
    return card, val

# calulates the sun of all your cards
def calculate_score(hand_values):
    
    total = sum(hand_values)
    
    # checks for aces
    aces = 0
    for num in hand_values:
        if num == 11:
            aces += 1

    #checks for busting with 11 value aces and reavalulates acordingly
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

# the player's turn
def game_loop(hand, hand_value, draw_deck):
    
    #checks if you have cards yet if not gives the player 2 cards
    if not hand:
        for _ in range(2):
            card, val = draw_card(draw_deck)
            hand.append(card)
            hand_value.append(val)

    # prints the player's hand for player calculation
    print(f"Your hand: {hand}")
    score = calculate_score(hand_value)

    # checks for busting
    if score > 21:
        print("You busted :(")
        return draw_deck, 0

    # checks if you already have 21 so the player don't accedentally bust with a black jack
    if score == 21:
        return draw_deck, score

    # Checks if the player wants to hit, if so it gives them a card if not ends their turn
    hit = input("Want to hit?(Y/N): ").strip().upper() #.strip().upper() auto removes spaces and capitize lowercase letters
    if hit == "Y":
        card, val = draw_card(draw_deck)
        hand.append(card)
        hand_value.append(val)
        return game_loop(
            hand, hand_value, draw_deck
        )
    else:
        return draw_deck, score

# the metaphorical dealer's turn
def dealers_turn(hand, hand_value, draw_deck, target_score):
    
    # same check for new hand
    if not hand:
        for _ in range(2):
            card, val = draw_card(draw_deck)
            hand.append(card)
            hand_value.append(val)

    # prints the Dealer's hand for visulization
    print(f"Dealer's hand: {hand}")
    score = calculate_score(hand_value)

    # checks if the dealer busted
    if score > 21:
        print("Dealer busted! :)")
        return

    # dealer checks if his hand is less than the avage of all active players if so he hits
    if score < target_score:
        print("Dealer hits...")
        card, val = draw_card(draw_deck)
        hand.append(card)
        hand_value.append(val)
        dealers_turn(hand, hand_value, draw_deck, target_score)
    else:
        print(f"Dealer stands with a score of {score}.")


# Execution
active_deck = deck.copy()

# Ask for the number of players
num_players = int(input("How many players are playing? ").strip())
player_scores = []

# Loop through each player
for i in range(num_players):
    print(f"\n--- Player {i + 1}'s Turn ---")
    active_deck, score = game_loop([], [], active_deck)
    player_scores.append(score)

# Filters out busted players by checking score to find non-busted scores
non_busted_scores = [s for s in player_scores if s > 0]

# Only play the dealer's turn if there is at least one non-busted player
if non_busted_scores:
    
    # Calculate the mean of all non-busted players
    mean_score = sum(non_busted_scores) / len(non_busted_scores)
    print(f"\n--- Dealer's Turn ---")
    dealers_turn([], [], active_deck, mean_score)
else:
    print("\nAll players busted! Dealer wins.")