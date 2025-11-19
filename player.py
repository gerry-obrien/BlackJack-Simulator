class Player:
    """
    A class to represent a Blackjack player or dealer.

    Attributes:
        name (str): The name of the player or dealer.
        hand (list): The list of cards in the player's hand.
        bankroll (int): The amount of money the player has (only for players).
    """

    def __init__(self, name="Player", bankroll=0):
        """
        Initialize a player or dealer.

        Args:
            name (str): Name of the player.
            bankroll (int): Initial bankroll for the player (default is 0).
        """
        self.name = name
        self.hand = []
        self.bankroll = bankroll

    def add_card(self, card):
        """
        Add a card to the player's hand.

        Args:
            card (tuple): A card represented as (rank, suit).
        """
        rank, suit = card
        # Only convert to integer if rank is a string and represents a number
        if isinstance(rank, str) and rank.isdigit():
            rank = int(rank)
        self.hand.append((rank, suit))

    def calculate_hand(self):
        """
        Calculate the total value of the player's hand.

        Aces are counted as 11 initially, but switch to 1 if the total exceeds 21.

        Returns:
            int: The total value of the player's hand.
        """
        total = 0
        aces = 0

        for card in self.hand:
            rank, _ = card
            if isinstance(rank, int):  # Numeric cards (2-10)
                total += rank
            elif rank in ['J', 'Q', 'K']:  # Face cards
                total += 10
            elif rank == 'A':  # Ace handling
                aces += 1
                total += 11

        # Adjust Aces from 11 to 1 if total exceeds 21
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def reset_hand(self):
        """
        Clear the player's hand at the end of a round.
        """
        self.hand = []
