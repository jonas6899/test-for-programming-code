import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.ascii_art = self.generate_ascii_art()

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def generate_ascii_art(self):
        # ASCII art representations for each card
        # You can replace these with actual ASCII art or customize as you like
        return f"""
        ┌───────┐
        │ {self.rank:<2}    │
        │       │
        │   {self.suit}   │
        │       │
        │    {self.rank:>2} │
        └───────┘
        """

class Deck:
    def __init__(self):
        self.cards = []
        for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:
            for rank in range(2, 11):
                self.cards.append(Card(suit, str(rank)))
            for rank in ['Jack', 'Queen', 'King', 'Ace']:
                self.cards.append(Card(suit, rank))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal_card(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        ace_count = 0
        for card in self.cards:
            if card.rank.isdigit():
                value += int(card.rank)
            elif card.rank in ['Jack', 'Queen', 'King']:
                value += 10
            else:
                ace_count += 1
                value += 11
        while value > 21 and ace_count:
            value -= 10
            ace_count -= 1
        return value

def print_hand(hand, dealer=False):
    if dealer:
        print("\nDealer's Hand:")
        print("<card hidden>")
        print(hand.cards[1].ascii_art)
    else:
        print("\nYour Hand:")
        for card in hand.cards:
            print(card.ascii_art)
        print("Value:", hand.get_value())

def play_blackjack(balance):
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()

    bet = int(input(f"Place your bet (Current Balance: ${balance}): "))
    while bet > balance:
        print("Insufficient balance. Please place a valid bet.")
        bet = int(input("Place your bet: "))

    balance -= bet

    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    print_hand(player_hand)
    print_hand(dealer_hand, dealer=True)

    while player_hand.get_value() < 21:
        choice = input("\nDo you want to hit (receive another card) or stand? (h/s): ").lower()
        if choice == 'h':
            player_hand.add_card(deck.deal_card())
            print_hand(player_hand)
            if player_hand.get_value() >= 21:
                break
        elif choice == 's':
            break
        else:
            print("Invalid choice. Please enter 'h' to hit or 's' to stand.")

    if player_hand.get_value() > 21:
        print("\nYou've exceeded 21. Dealer wins.")
        return balance

    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
    
    print_hand(player_hand)
    print_hand(dealer_hand)

    if dealer_hand.get_value() > 21 or player_hand.get_value() > dealer_hand.get_value():
        winnings = bet * 2
        balance += winnings
        print(f"\nCongratulations! You win and earn ${winnings}. Current Balance: ${balance}")
    elif dealer_hand.get_value() > player_hand.get_value():
        print("\nDealer wins!")
    else:
        balance += bet
        print(f"\nIt's a tie! You get your bet back. Current Balance: ${balance}")

    return balance

def main():
    balance = 100  # Initial player balance
    continue_playing = True

    while continue_playing and balance > 0:
        balance = play_blackjack(balance)
        if balance < 10:
            print("Sorry, you've run out of money. Game over!")
            break
        else:
            choice = input("\nWould you like to continue playing or cash out? (p/c): ").lower()
            if choice == 'c':
                print(f"You are leaving the table with ${balance}.")
                continue_playing = False

main()