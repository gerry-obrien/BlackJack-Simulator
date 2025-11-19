from deck import Deck
from player import Player
from utils import display_hand

class BlackjackGame:
    """
    A class to manage the flow of a Blackjack game with advanced rules.

    Attributes:
        deck (Deck): A Deck object for managing cards.
        player (Player): The player object.
        dealer (Player): The dealer object.
        min_bet (float): Minimum bet amount for each round.
    """

    def __init__(self):
        """
        Initialize the Blackjack game with a deck, player, and dealer.
        """
        self.deck = Deck()
        self.player = Player("Player", bankroll=1000.00)
        self.dealer = Player("Dealer")
        self.min_bet = 10.00

    def start(self):
        """
        Start and manage the game loop until the player decides to quit or runs out of money.
        """
        print("\nWelcome to Advanced Blackjack!\n")

        while True:
            if self.player.bankroll <= 0:
                print("You are out of money!")
                restart = input("Do you want to restart with €1000? (y/n): ").strip().lower()
                if restart == 'y':
                    self.player.bankroll = 1000.00
                    print("\nBankroll reset to €1000. Let's play again!\n")
                else:
                    print("Thanks for playing Blackjack! Goodbye!")
                    break

            print(f"Your current bankroll: €{self.player.bankroll:.2f}")

            # Get the player's bet
            while True:
                try:
                    bet = float(input(f"Enter your bet (minimum €{self.min_bet:.2f}): "))
                    if bet < self.min_bet:
                        print(f"Bet must be at least €{self.min_bet:.2f}.")
                    elif bet > self.player.bankroll:
                        print("You don't have enough money for that bet.")
                    else:
                        break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            # Play a single hand
            self.play_hand(bet)

            print(f"Updated bankroll: €{self.player.bankroll:.2f}")
            cont = input("Play another hand? (y/n): ").strip().lower()
            if cont != 'y':
                print("Thanks for playing Blackjack! Goodbye!")
                break

    def play_hand(self, bet):
        """
        Play a single hand of Blackjack.

        Args:
            bet (float): The bet amount for this round.
        """
        self.deck = Deck()
        self.player.reset_hand()
        self.dealer.reset_hand()

        # Deduct the initial bet from the bankroll
        self.player.bankroll -= bet
        print(f"Initial bet of €{bet:.2f} placed. Current bankroll: €{self.player.bankroll:.2f}")

        # Initial deal
        for _ in range(2):
            self.player.add_card(self.deck.deal_card())
            self.dealer.add_card(self.deck.deal_card())

        # Display initial hands
        display_hand(self.player, hide_first=False)
        display_hand(self.dealer, hide_first=True)

        # Insurance Logic
        insurance_bet = 0
        if self.dealer.hand[0][0] == 'A':  # Check if dealer's face-up card is an Ace
            insurance = input("Do you want to take insurance? (y/n): ").strip().lower()
            if insurance == 'y':
                insurance_bet = bet / 2
                print(f"Insurance bet of €{insurance_bet:.2f} placed.")
                # Check if dealer has Blackjack
                if self.dealer.calculate_hand() == 21:
                    print("Dealer has Blackjack! Insurance bet paid 2:1.")
                    self.player.bankroll += 2* insurance_bet  # Refund insurance bet
                    return  # End round as dealer wins with Blackjack
                else:
                    print("Dealer does not have Blackjack. Insurance bet is lost.")
                    self.player.bankroll -= insurance_bet  # Deduct insurance bet

        # Continue normal gameplay after insurance resolution
        if self.player.calculate_hand() == 21:
            print("Blackjack! You are paid 3:2.")
            self.player.bankroll += 1.5 * bet
            return

        doubled = False
        while True:
            print("\nActions: [h]it, [s]tand, [r]surrender")
            if len(self.player.hand) == 2:
                print("[d]ouble down")
            if self.can_split():
                print("[p]split")

            action = input("Choose your action: ").strip().lower()

            # Hit
            if action == 'h':
                self.player.add_card(self.deck.deal_card())
                display_hand(self.player, hide_first=False)
                if self.player.calculate_hand() > 21:
                    print("Bust! You lose this round.")
                    self.player.bankroll -= bet
                    return

            # Stand
            elif action == 's':
                break

            # Surrender
            elif action == 'r':
                print("You surrendered. Half your bet is refunded.")
                self.player.bankroll -= bet / 2
                return

            # Double Down
            elif action == 'd' and len(self.player.hand) == 2:
                print("You chose to double down!")
                self.player.bankroll -= bet
                bet *= 2
                self.player.add_card(self.deck.deal_card())
                display_hand(self.player, hide_first=False)
                doubled = True
                break

            # Split
            elif action == 'p' and self.can_split():
                print("You chose to split!")
                self.handle_split(bet)
                return

            else:
                print("Invalid action. Please choose again.")

        # Dealer's turn
        print("\nDealer's Turn:")
        while self.dealer.calculate_hand() < 17:
            self.dealer.add_card(self.deck.deal_card())
        display_hand(self.dealer, hide_first=False)

        # Determine winner
        self.check_winner(bet, doubled)

    def handle_single_hand(self, bet):
        """
        Handle a single hand (no split).

        Args:
            bet (float): The bet amount for this round.
        """
        while True:
            print("\nActions: [h]it, [s]tand, [r]surrender")
            if len(self.player.hand) == 2:
                print("[d]ouble down")

            action = input("Choose your action: ").strip().lower()

            # Hit
            if action == 'h':
                self.player.add_card(self.deck.deal_card())
                display_hand(self.player, hide_first=False)
                if self.player.calculate_hand() > 21:
                    print("Bust! You lose this round.")
                    self.player.bankroll -= bet
                    return

            # Stand
            elif action == 's':
                break

            # Surrender
            elif action == 'r':
                self.player.bankroll -= bet / 2
                print("You surrendered! You get back half your bet.")
                return

            # Double Down
            elif action == 'd' and len(self.player.hand) == 2:
                self.player.bankroll -= bet
                bet *= 2
                self.player.add_card(self.deck.deal_card())
                display_hand(self.player, hide_first=False)
                print("You doubled down! Your turn ends.")
                break

            else:
                print("Invalid action. Please choose again.")

    def handle_split(self, bet):
        """
        Handle splitting the player's hand into two separate hands.

        Args:
            bet (float): The bet amount for the original hand.
        """
        card1 = self.player.hand[0]
        card2 = self.player.hand[1]

        # Deduct the additional bet for the second hand
        self.player.bankroll -= bet
        print(f"Additional split bet of €{bet:.2f} deducted. Current bankroll: €{self.player.bankroll:.2f}")

        # Create two separate hands for the split
        hand1 = [card1]
        hand2 = [card2]

        # Play the first split hand
        print(f"\n--- Playing Hand 1 (Bet: €{bet:.2f}) ---")
        total1 = self.play_split_hand(hand1)

        # Play the second split hand
        print(f"\n--- Playing Hand 2 (Bet: €{bet:.2f}) ---")
        total2 = self.play_split_hand(hand2)

        # Dealer's turn to complete the round for split hands
        dealer_total = self.dealer_turn_for_split()

        # Resolve both hands separately and adjust bankroll based on results
        self.adjust_split_results(hand1, dealer_total, bet, "Hand 1")
        self.adjust_split_results(hand2, dealer_total, bet, "Hand 2")

    def play_split_hand(self, hand):
        """
        Play a single split hand and return the total value.

        Args:
            hand (list): The cards in the split hand.

        Returns:
            int: The total value of the hand.
        """
        while True:
            print("\nYour current hand:")
            for card in hand:
                print(f"{card[0]}{card[1]}", end="  ")
            total = self.calculate_hand_value(hand)
            print(f"  Total: {total}")

            if total > 21:  # Bust
                print("Bust! You lose this hand.")
                return total

            action = input("Do you want to [h]it or [s]tand? ").strip().lower()
            if action == 'h':
                hand.append(self.deck.deal_card())
            elif action == 's':
                break
            else:
                print("Invalid action. Please choose [h]it or [s]tand.")
        return total


    def dealer_turn_for_split(self):
        """
        Perform the dealer's turn for split hands.

        Returns:
            int: The dealer's final hand value.
        """
        print("\nDealer's Turn:")
        while self.dealer.calculate_hand() < 17:
            self.dealer.add_card(self.deck.deal_card())
        display_hand(self.dealer, hide_first=False)
        return self.dealer.calculate_hand()

    def adjust_split_results(self, hand, dealer_total, bet, hand_label):
        """
        Adjust the bankroll based on the result of a split hand.

        Args:
            hand (list): The player's split hand.
            dealer_total (int): The dealer's total hand value.
            bet (float): The bet amount for this hand.
            hand_label (str): Label for the hand being resolved (e.g., "Hand 1").
        """
        result = self.resolve_split_hand(hand, dealer_total, bet)
        print(f"{hand_label} Result: {result}")  # Debugging statement

        if result == "Win":
            self.player.bankroll += 2 * bet  # Return the initial bet + profit
            print(f"{hand_label}: Won €{bet:.2f}")
        elif result == "Tie":
            self.player.bankroll += bet  # Refund the initial bet
            print(f"{hand_label}: Tied, refunded €{bet:.2f}")
        elif result == "Lose":
            # Bet already deducted during split
            print(f"{hand_label}: Lost €{bet:.2f}")
        print(f"Bankroll after {hand_label}: €{self.player.bankroll:.2f}")  # Debugging statement



    def resolve_split_hand(self, hand, dealer_total, bet):
        """
        Resolve the outcome of a split hand against the dealer.

        Args:
            hand (list): The player's split hand.
            dealer_total (int): The dealer's total hand value.
            bet (float): The bet amount for this hand.

        Returns:
            str: The result of the hand ('Win', 'Lose', or 'Tie').
        """
        player_total = self.calculate_hand_value(hand)

        if player_total > 21:
            # Player busts, bet is lost
            return "Lose"
        elif dealer_total > 21 or player_total > dealer_total:
            # Player wins
            return "Win"
        elif player_total < dealer_total:
            # Dealer wins
            return "Lose"
        else:
            # Tie
            return "Tie"

    def check_winner(self, bet, doubled=False):
        """
        Determine the winner of the hand.

        Args:
            bet (float): The original bet amount.
            doubled (bool): Whether the player doubled down.
        """
        # Adjust the bet if the player doubled down
        effective_bet = bet * 2 if doubled else bet

        player_total = self.player.calculate_hand()
        dealer_total = self.dealer.calculate_hand()

        if player_total > 21:
            print("Bust! You lose this round.")  # Bet already deducted at the start
        elif dealer_total > 21 or player_total > dealer_total:
            print("You win this round!")
            self.player.bankroll += 2 * effective_bet  # Return the initial bet + profit
        elif player_total < dealer_total:
            print("Dealer wins this round.")  # Bet already deducted at the start
        else:
            print("It's a tie!")
            self.player.bankroll += effective_bet  # Refund the initial bet

    def can_split(self):
        """
        Check if the player can split their hand.

        Returns:
            bool: True if split is possible, False otherwise.
        """
        return len(self.player.hand) == 2 and (self.player.hand[0][0] == self.player.hand[1][0] or (
                    self.player.hand[0][0] in ['J', 'Q', 'K', 10] and self.player.hand[1][0] in ['J', 'Q', 'K', 10]))

    def calculate_hand_value(self, hand):
        """
        Calculate the value of a given hand.

        Args:
            hand (list): The hand whose value needs to be calculated.

        Returns:
            int: The total value of the hand.
        """
        total = 0
        aces = 0
        for card in hand:
            rank, _ = card
            if isinstance(rank, int):
                total += rank
            elif rank in ['J', 'Q', 'K']:
                total += 10
            elif rank == 'A':
                aces += 1
                total += 11

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total


