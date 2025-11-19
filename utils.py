def display_hand(player, hide_first=False):
    """
    Display a player's or dealer's hand.

    Args:
        player (Player): The player whose hand is displayed.
        hide_first (bool): Whether to hide the first card (for the dealer).
    """
    print(f"\n{player.name}'s Hand:")

    if hide_first and player.name == "Dealer":
        # Show only the first card for the dealer
        print(f"{player.hand[0][0]}{player.hand[0][1]}  [Hidden]")
    else:
        # Show all cards for the player or the dealer's revealed hand
        for card in player.hand:
            print(f"{card[0]}{card[1]}", end="  ")
        print(f"  Total: {player.calculate_hand()}")

    print()
