import random

class Deck:
    """
    A class to represent a deck of cards in Blackjack.
    """

    def __init__(self, predefined_cards=None):
        """
        Initialize the deck. If predefined_cards is provided, use it instead of shuffling.
        Args:
            predefined_cards (list): A list of cards to use for testing.
        """
        if predefined_cards:
            self.cards = predefined_cards  # Testing mode
        else:
            self.cards = [
                (rank, suit) for suit in ['♠', '♥', '♦', '♣']
                for rank in list(range(2, 11)) + ['J', 'Q', 'K', 'A']
            ]
            self.shuffle()

    def shuffle(self):
        """Shuffle the deck of cards randomly."""
        random.shuffle(self.cards)

    def deal_card(self):
        """Deal one card from the top of the deck."""
        return self.cards.pop() if self.cards else None
