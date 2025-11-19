import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

from game import BlackjackGame

class BlackjackGUI:
    """
    A class to implement the graphical user interface (GUI) for the Blackjack game.

    Attributes:
        root (tk.Tk): The root window for the GUI.
        game (BlackjackGame): An instance of the game logic.
        split_hands (list): List to track split hands for the player.
        current_hand_index (int): Index of the current active hand for split hands.
        current_bet (float): The current bet placed by the player.
        insurance_bet (float): The insurance bet amount (if applicable).
        has_hit_or_split (bool): Flag to track if the player has hit or split.
        did_double (bool): Flag to track if the player doubled down.
        card_images (dict): Preloaded card images for the GUI.
    """

    def __init__(self, root):
        """
        Initialize the Blackjack GUI with the root window and game instance.
        Set up the GUI layout, including frames, labels, and buttons.
        """
        self.root = root
        self.root.title("Blackjack")

        # Create an instance of the BlackjackGame logic
        self.game = BlackjackGame()

        # Attributes for handling split hands and bets
        self.split_hands = []
        self.current_hand_index = 0
        self.current_bet = 0.0
        self.insurance_bet = 0.0

        # Flags for player actions
        self.has_hit_or_split = False
        self.did_double = False

        # Preload card images for display
        self.card_images = self.load_card_images()

        # -------------- GUI Layout Setup --------------
        # Top frame: Quit button, Bankroll display, Bet input, Deal button
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, pady=10)

        self.quit_button = tk.Button(
            self.top_frame,
            text="Quit",
            width=8,
            command=self.on_quit
        )
        self.quit_button.pack(side=tk.LEFT, padx=10)

        self.bankroll_label = tk.Label(
            self.top_frame,
            text=f"Bankroll: €{self.game.player.bankroll:.2f}",
            font=("Arial", 12, "bold")
        )
        self.bankroll_label.pack(side=tk.LEFT, padx=10)

        self.bet_label = tk.Label(self.top_frame, text="Bet: ")
        self.bet_label.pack(side=tk.LEFT)

        self.bet_entry = tk.Entry(self.top_frame, width=7)
        self.bet_entry.pack(side=tk.LEFT)
        self.bet_entry.insert(0, "10")  # Default bet

        self.deal_button = tk.Button(self.top_frame, text="Deal", command=self.on_deal)
        self.deal_button.pack(side=tk.LEFT, padx=10)

        # Middle frame: Dealer and Player areas
        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.pack(side=tk.TOP, pady=10)

        self.dealer_frame = tk.LabelFrame(self.middle_frame, text="Dealer", padx=10, pady=10)
        self.dealer_frame.pack(side=tk.TOP, padx=10, pady=10)

        self.player_area_frame = tk.Frame(self.middle_frame)
        self.player_area_frame.pack(side=tk.TOP, padx=10, pady=10)

        # Dealer’s labels for cards and total
        self.dealer_card_labels = []
        self.dealer_total_label = None

        # Player frames (to support split hands)
        self.player_hand_frames = []
        self.player_hand_card_labels = []

        # Bottom frame: Action buttons
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.BOTTOM, pady=10)

        self.button_frame = tk.Frame(self.bottom_frame)
        self.button_frame.pack(side=tk.TOP)

        # Action buttons
        self.hit_button = tk.Button(self.button_frame, text="Hit", width=10, command=self.on_hit)
        self.stand_button = tk.Button(self.button_frame, text="Stand", width=10, command=self.on_stand)
        self.double_button = tk.Button(self.button_frame, text="Double", width=10, command=self.on_double)
        self.surrender_button = tk.Button(self.button_frame, text="Surrender", width=10, command=self.on_surrender)
        self.split_button = tk.Button(self.button_frame, text="Split", width=10, command=self.on_split)

        # Initially hide the action buttons
        self.hide_action_buttons()


    def load_card_images(self):
        """
        Load all .png card images from the 'cards' folder and resize them for display.

        Returns:
            dict: A dictionary mapping card keys to their respective tkinter PhotoImage objects.
        """
        card_images = {}
        folder_path = os.path.join(os.path.dirname(__file__), "cards")

        for file_name in os.listdir(folder_path):
            if file_name.endswith(".png"):
                base_name = file_name[:-4]  # Remove '.png' extension
                full_path = os.path.join(folder_path, file_name)

                # Load and resize the image
                pil_img = Image.open(full_path).resize((80, 120), Image.LANCZOS)
                tk_img = ImageTk.PhotoImage(pil_img)

                # Add the image to the dictionary
                card_images[base_name] = tk_img

        return card_images

    def get_card_image_key(self, card):
        """
        Generate the key for accessing the appropriate card image.

        Args:
            card (tuple): A tuple representing the card (rank, suit), e.g., ('10', '♠').

        Returns:
            str: The key for the card image, e.g., '10_spade' or 'jack_heart'.
        """
        rank, suit = card
        if rank == 'A':
            rank_str = "1"
        elif rank == 'J':
            rank_str = "jack"
        elif rank == 'Q':
            rank_str = "queen"
        elif rank == 'K':
            rank_str = "king"
        else:
            rank_str = str(rank)

        suit_map = {'♠': 'spade', '♥': 'heart', '♦': 'diamond', '♣': 'club'}
        suit_str = suit_map.get(suit, 'spade')  # Default to 'spade' if suit is invalid

        return f"{rank_str}_{suit_str}"


    def on_quit(self):
        """
        Handles the quit button functionality. Closes the game window.
        """
        self.root.destroy()

    def check_for_cash_in_after_hand(self):
        """
        Checks if the player's bankroll is below the minimum bet after a hand.
        If bankroll < 10, prompts the player to reset their bankroll to €1000.
        Updates the bankroll label immediately if reset is chosen.
        """
        if self.game.player.bankroll < 10:
            answer = messagebox.askyesno("Cash In?", "Your bankroll is below 10.\nReset to €1000?")
            if answer:
                self.game.player.bankroll = 1000.0
                self.update_bankroll_label()  # Update the bankroll display immediately


    def on_deal(self):
        """
        Handles the logic for starting a new round.
        - Clears the table and resets hands and bets.
        - Validates the player's bet and updates the bankroll.
        - Deals initial cards to the player and dealer.
        - Prompts for insurance if the dealer's upcard is an Ace.
        - Checks for an immediate Blackjack and pays out if applicable.
        """
        # Clear table and reset relevant attributes
        self.clear_table()
        self.split_hands = []
        self.current_hand_index = 0
        self.insurance_bet = 0.0
        self.has_hit_or_split = False
        self.did_double = False

        # Validate bet input
        try:
            bet = float(self.bet_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid bet. Please enter a valid number.")
            return

        if bet < self.game.min_bet:
            messagebox.showerror("Error", f"Bet must be at least €{self.game.min_bet:.2f}.")
            return
        if bet > self.game.player.bankroll:
            messagebox.showerror("Error", "Not enough bankroll for that bet.")
            return

        self.current_bet = bet
        # Deduct the bet upfront
        self.game.player.bankroll -= bet
        self.update_bankroll_label()

        # Reinitialize the deck and reset hands
        self.game.deck = self.game.deck.__class__()  # New deck instance
        self.game.player.reset_hand()
        self.game.dealer.reset_hand()

        # Deal initial cards
        self.game.player.add_card(self.game.deck.deal_card())  # Player Card 1
        self.game.dealer.add_card(self.game.deck.deal_card())  # Dealer Card 1 (hidden)
        self.game.player.add_card(self.game.deck.deal_card())  # Player Card 2
        self.game.dealer.add_card(self.game.deck.deal_card())  # Dealer Card 2 (visible)

        # Display initial cards
        self.display_dealer_cards(hide_first=True)
        self.display_player_cards()

        # Offer insurance if the dealer's visible card is an Ace
        dealer_upcard = self.game.dealer.hand[1]
        if dealer_upcard[0] == 'A':
            answer = messagebox.askyesno("Insurance?", "Dealer shows an Ace. Take insurance?")
            if answer:
                self.handle_insurance()

        self.show_action_buttons()

        # Check for immediate Blackjack
        if self.game.player.calculate_hand() == 21:
            messagebox.showinfo("Blackjack!", "You got Blackjack! 3:2 payout.")
            self.game.player.bankroll += 2.5 * bet  # 3:2 payout
            self.update_bankroll_label()
            self.hide_action_buttons()
            self.check_for_cash_in_after_hand()

    def handle_insurance(self):
        """
        Handles the insurance logic if the dealer's visible card is an Ace.
        Deducts the insurance bet from the player's bankroll.
        Resolves the insurance bet based on whether the dealer has Blackjack.
        """
        insurance_amount = self.current_bet / 2.0
        if self.game.player.bankroll < insurance_amount:
            messagebox.showwarning("Warning", "Not enough bankroll for insurance.")
            return

        # Deduct insurance bet
        self.game.player.bankroll -= insurance_amount
        self.insurance_bet = insurance_amount
        self.update_bankroll_label()

        # Calculate dealer's hand value
        dealer_total = self.game.dealer.calculate_hand()
        player_total = self.game.player.calculate_hand()

        if dealer_total == 21:
            # Dealer has Blackjack
            self.display_dealer_cards(hide_first=False)
            if player_total == 21:
                # Both player and dealer have Blackjack
                messagebox.showinfo("Dealer Blackjack", "Dealer has Blackjack, but you also have 21.\n"
                                                        "Main bet is pushed, insurance pays 2:1 => profit!")
                self.game.player.bankroll += self.current_bet  # Refund main bet
            else:
                messagebox.showinfo("Dealer Blackjack",
                    "Dealer has Blackjack. Main bet lost, but insurance pays 2:1 => net 0.")
            self.game.player.bankroll += self.insurance_bet * 3  # Insurance pays 2:1
            self.update_bankroll_label()
            self.hide_action_buttons()
            self.check_for_cash_in_after_hand()
        else:
            # Dealer does not have Blackjack
            messagebox.showinfo("Insurance", "Dealer does not have Blackjack. You lose the insurance bet.\n"
                                             "Continue playing your main bet.")


    def on_hit(self):
        """
        Handles the "Hit" action for the player.
        - Adds a card to the player's current hand.
        - Checks for bust conditions and manages split hands if in split mode.
        """
        self.has_hit_or_split = True
        if self.in_split_mode():
            current_hand = self.split_hands[self.current_hand_index]
            current_hand.append(self.game.deck.deal_card())
            self.display_player_cards()
            if self.game.calculate_hand_value(current_hand) > 21:
                messagebox.showinfo("Bust", f"Hand {self.current_hand_index + 1} busts!")
                self.on_stand()  # Move to the next hand
        else:
            self.game.player.add_card(self.game.deck.deal_card())
            self.display_player_cards()
            if self.game.player.calculate_hand() > 21:
                messagebox.showinfo("Bust", "You busted!")
                self.hide_action_buttons()
                self.check_for_cash_in_after_hand()  # End of round, check bankroll

    def on_stand(self):
        """
        Handles the "Stand" action for the player.
        - Ends the player's turn for the current hand.
        - If in split mode, moves to the next hand or finishes the round.
        - Otherwise, starts the dealer's turn.
        """
        self.has_hit_or_split = True
        if self.in_split_mode():
            if self.current_hand_index < len(self.split_hands) - 1:
                self.current_hand_index += 1  # Move to the next split hand
                self.display_player_cards()
            else:
                self.finish_split_round()  # Resolve split hands
        else:
            self.dealer_play()  # Dealer's turn

    def on_double(self):
        """
        Handles the "Double Down" action for the player.
        - Doubles the player's bet and deducts it from the bankroll.
        - Adds one additional card to the player's hand and ends their turn.
        """
        if self.has_hit_or_split:
            messagebox.showinfo("Double", "You can only double with your first two cards.")
            return

        try:
            bet = float(self.bet_entry.get())
        except ValueError:
            bet = self.game.min_bet

        if self.game.player.bankroll < bet:
            messagebox.showwarning("Warning", "Not enough bankroll to double.")
            return

        # Deduct the additional bet for doubling
        self.game.player.bankroll -= bet
        self.update_bankroll_label()
        self.did_double = True
        self.has_hit_or_split = True

        if self.in_split_mode():
            current_hand = self.split_hands[self.current_hand_index]
            current_hand.append(self.game.deck.deal_card())
            self.display_player_cards()
            if self.game.calculate_hand_value(current_hand) > 21:
                messagebox.showinfo("Bust", f"Hand {self.current_hand_index + 1} busts!")
            self.on_stand()  # Auto-stand after doubling
        else:
            self.game.player.add_card(self.game.deck.deal_card())
            self.display_player_cards()
            if self.game.player.calculate_hand() > 21:
                messagebox.showinfo("Bust", "You busted!")
                self.hide_action_buttons()
                self.check_for_cash_in_after_hand()
            else:
                self.dealer_play()  # Auto-stand after doubling

    def on_surrender(self):
        """
        Handles the "Surrender" action for the player.
        - Refunds half the player's bet.
        - Ends the round immediately.
        """
        self.has_hit_or_split = True
        refund = self.current_bet / 2.0
        self.game.player.bankroll += refund
        messagebox.showinfo("Surrender", f"You surrendered, got €{refund:.2f} back.")
        self.hide_action_buttons()
        self.update_bankroll_label()
        self.check_for_cash_in_after_hand()

    def on_split(self):
        """
        Handles the "Split" action for the player.
        - Splits the player's hand into two separate hands.
        - Deducts an additional bet for the second hand.
        """
        self.has_hit_or_split = True
        if not self.game.can_split():
            messagebox.showwarning("Warning", "Cannot split these cards.")
            return

        try:
            bet = float(self.bet_entry.get())
        except ValueError:
            bet = self.game.min_bet

        if self.game.player.bankroll < bet:
            messagebox.showwarning("Warning", "Not enough bankroll to split.")
            return

        # Deduct the bet for the split
        self.game.player.bankroll -= bet
        self.update_bankroll_label()

        # Split the hand into two separate hands
        card1, card2 = self.game.player.hand[0], self.game.player.hand[1]
        hand1 = [card1]
        hand2 = [card2]
        self.split_hands = [hand1, hand2]
        self.current_hand_index = 0

        messagebox.showinfo("Split", "You split your hand into two!")
        self.game.player.hand = []
        self.display_player_cards()


    def dealer_play(self):
        """
        Handles the dealer's turn in a single-hand scenario.
        - Dealer draws cards until their total is at least 17.
        - Resolves the round by checking the winner.
        """
        self.hide_action_buttons()
        while self.game.dealer.calculate_hand() < 17:
            self.game.dealer.add_card(self.game.deck.deal_card())
        self.display_dealer_cards(hide_first=False)
        self.check_winner(doubled=self.did_double)

    def finish_split_round(self):
        """
        Handles the resolution of split hands.
        - Dealer completes their turn.
        - Each hand is individually resolved and winnings/losses are updated.
        """
        self.hide_action_buttons()
        while self.game.dealer.calculate_hand() < 17:
            self.game.dealer.add_card(self.game.deck.deal_card())
        self.display_dealer_cards(hide_first=False)

        dealer_total = self.game.dealer.calculate_hand()
        for i, hand in enumerate(self.split_hands):
            player_total = self.game.calculate_hand_value(hand)
            if player_total > 21:
                outcome = "Bust"
            elif dealer_total > 21 or player_total > dealer_total:
                outcome = "Win"
                self.game.player.bankroll += 2 * self.current_bet
            elif player_total < dealer_total:
                outcome = "Lose"
            else:
                outcome = "Tie"
                self.game.player.bankroll += self.current_bet

            messagebox.showinfo(f"Hand {i + 1} Result",
                f"Hand {i + 1} -> {outcome}.\nYour total: {player_total}, Dealer: {dealer_total}")

        self.update_bankroll_label()
        self.check_for_cash_in_after_hand()

    def check_winner(self, doubled=False):
        """
        Resolves the outcome of a single-hand round.
        - Compares player and dealer totals to determine the winner.
        - Updates bankroll based on results.
        """
        effective_bet = self.current_bet * 2 if doubled else self.current_bet
        player_total = self.game.player.calculate_hand()
        dealer_total = self.game.dealer.calculate_hand()

        if player_total > 21:
            messagebox.showinfo("Result", "Player busts! Dealer wins.")
        elif dealer_total > 21 or player_total > dealer_total:
            self.game.player.bankroll += 2 * effective_bet
            messagebox.showinfo("Result", "You win!")
        elif dealer_total > player_total:
            messagebox.showinfo("Result", "Dealer wins!")
        else:
            self.game.player.bankroll += effective_bet
            messagebox.showinfo("Result", "Push (tie).")

        self.update_bankroll_label()
        self.check_for_cash_in_after_hand()


    def display_dealer_cards(self, hide_first=True):
        """
        Displays the dealer's cards on the GUI.
        If `hide_first` is True, the first card is displayed as hidden (face down).

        Args:
            hide_first (bool): Whether to hide the dealer's first card.
        """
        # Clear previous dealer card labels
        for lbl in self.dealer_card_labels:
            lbl.destroy()
        self.dealer_card_labels.clear()

        # Remove the previous dealer total label if it exists
        if self.dealer_total_label:
            self.dealer_total_label.destroy()
            self.dealer_total_label = None

        visible_cards = []  # To calculate visible card totals
        for i, card in enumerate(self.game.dealer.hand):
            if i == 0 and hide_first:
                # Display hidden card or a fallback message
                back_img = self.card_images.get("back")
                if back_img:
                    lbl = tk.Label(self.dealer_frame, image=back_img)
                    lbl.image = back_img
                else:
                    lbl = tk.Label(self.dealer_frame, text="[Hidden]", font=("Arial", 14, "bold"))
            else:
                # Display the visible card with its image or a text fallback
                key = self.get_card_image_key(card)
                img = self.card_images.get(key)
                if img:
                    lbl = tk.Label(self.dealer_frame, image=img)
                    lbl.image = img
                else:
                    lbl = tk.Label(self.dealer_frame, text=f"{card[0]}{card[1]}", font=("Arial", 14, "bold"))
                visible_cards.append(card)

            lbl.pack(side=tk.LEFT, padx=2)
            self.dealer_card_labels.append(lbl)

        # Calculate and display the dealer's total
        if hide_first:
            if visible_cards:
                partial_total = self.game.calculate_hand_value(visible_cards)
                total_str = f"Total: {partial_total}"
            else:
                total_str = "Total: ???"
        else:
            dealer_total = self.game.dealer.calculate_hand()
            total_str = f"Total: {dealer_total}"

        self.dealer_total_label = tk.Label(self.dealer_frame, text=total_str, font=("Arial", 12, "bold"))
        self.dealer_total_label.pack(side=tk.LEFT, padx=10)

    def display_player_cards(self):
        """
        Displays the player's cards on the GUI, supporting single and split hands.
        - In split mode, displays each hand separately, marking the active hand.
        - In single-hand mode, displays the player's current hand.

        Supports card images or text-based fallbacks for missing card images.
        """
        # Clear previous player hand displays
        for frame in self.player_hand_frames:
            frame.destroy()
        self.player_hand_frames.clear()
        self.player_hand_card_labels.clear()

        if self.in_split_mode():
            # Handle split hands
            for idx, hand in enumerate(self.split_hands):
                # Frame title indicates active hand
                frame_text = f"Player Hand {idx + 1}"
                if idx == self.current_hand_index:
                    frame_text += " (Active)"

                hand_frame = tk.LabelFrame(self.player_area_frame, text=frame_text, padx=10, pady=10)
                hand_frame.pack(side=tk.LEFT, padx=10)

                labels_for_this_hand = []
                for card in hand:
                    key = self.get_card_image_key(card)
                    img = self.card_images.get(key)
                    if img:
                        lbl = tk.Label(hand_frame, image=img)
                        lbl.image = img
                    else:
                        lbl = tk.Label(hand_frame, text=f"{card[0]}{card[1]}", font=("Arial", 14, "bold"))
                    lbl.pack(side=tk.LEFT, padx=2)
                    labels_for_this_hand.append(lbl)

                # Display hand total
                hand_total = self.game.calculate_hand_value(hand)
                tk.Label(hand_frame, text=f"Total: {hand_total}", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

                self.player_hand_frames.append(hand_frame)
                self.player_hand_card_labels.append(labels_for_this_hand)
        else:
            # Handle single hand
            player_frame = tk.LabelFrame(self.player_area_frame, text="Player", padx=10, pady=10)
            player_frame.pack(side=tk.LEFT, padx=10)

            labels_for_this_hand = []
            for card in self.game.player.hand:
                key = self.get_card_image_key(card)
                img = self.card_images.get(key)
                if img:
                    lbl = tk.Label(player_frame, image=img)
                    lbl.image = img
                else:
                    lbl = tk.Label(player_frame, text=f"{card[0]}{card[1]}", font=("Arial", 14, "bold"))
                lbl.pack(side=tk.LEFT, padx=2)
                labels_for_this_hand.append(lbl)

            # Display player total
            player_total = self.game.player.calculate_hand()
            tk.Label(player_frame, text=f"Total: {player_total}", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

            self.player_hand_frames.append(player_frame)
            self.player_hand_card_labels.append(labels_for_this_hand)

    def in_split_mode(self):
        """
        Checks whether the player is currently in split mode (has split hands).

        Returns:
            bool: True if the player has split hands, False otherwise.
        """
        return len(self.split_hands) > 0

    def clear_table(self):
        """
        Clears the table by removing all displayed cards and totals for both the dealer and the player.
        Resets the labels and frames for a fresh start in a new round.
        """
        # Clear dealer's cards and total
        for lbl in self.dealer_card_labels:
            lbl.destroy()
        self.dealer_card_labels.clear()
        if self.dealer_total_label:
            self.dealer_total_label.destroy()
            self.dealer_total_label = None

        # Clear player's cards and hands
        for frame in self.player_hand_frames:
            frame.destroy()
        self.player_hand_frames.clear()
        self.player_hand_card_labels.clear()

    def hide_action_buttons(self):
        """
        Hides all action buttons (Hit, Stand, Double, Surrender, Split) from the GUI.
        Used when the player's turn ends or during transitions.
        """
        self.hit_button.pack_forget()
        self.stand_button.pack_forget()
        self.double_button.pack_forget()
        self.surrender_button.pack_forget()
        self.split_button.pack_forget()

    def show_action_buttons(self):
        """
        Displays the appropriate action buttons based on the current game state.
        - Hit and Stand are always available.
        - Double and Split are only shown if applicable (first turn, specific conditions).
        - Surrender is always available.
        """

        # Helper function for hover effects
        def add_hover_effect(button, hover_color="lightblue", default_color="SystemButtonFace"):
            """
            Adds a hover effect to a button.

            Args:
                button (tk.Button): The button to apply the effect on.
                hover_color (str): Background color on hover.
                default_color (str): Default background color when not hovered.
            """

            def on_enter(event):
                button.config(bg=hover_color)

            def on_leave(event):
                button.config(bg=default_color)

            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)

        # Ensure buttons are located and styled properly
        self.hit_button.config(width=12, height=2, font=("Arial", 14))
        self.stand_button.config(width=12, height=2, font=("Arial", 14))
        self.double_button.config(width=12, height=2, font=("Arial", 14))
        self.surrender_button.config(width=12, height=2, font=("Arial", 14))
        self.split_button.config(width=12, height=2, font=("Arial", 14))

        # Add hover effects to all buttons
        add_hover_effect(self.hit_button)
        add_hover_effect(self.stand_button)
        add_hover_effect(self.double_button)
        add_hover_effect(self.surrender_button)
        add_hover_effect(self.split_button)

        # Display buttons with proper spacing
        self.hit_button.pack(side=tk.LEFT, padx=10)
        self.stand_button.pack(side=tk.LEFT, padx=10)

        # Show Double button if applicable
        if (not self.in_split_mode()) and len(self.game.player.hand) == 2 and (not self.has_hit_or_split):
            self.double_button.pack(side=tk.LEFT, padx=10)

        # Show Surrender button
        self.surrender_button.pack(side=tk.LEFT, padx=10)

        # Show Split button if applicable
        if (not self.in_split_mode()) and self.game.can_split() and (not self.has_hit_or_split):
            self.split_button.pack(side=tk.LEFT, padx=10)

    def update_bankroll_label(self):
        """
        Updates the bankroll label in the GUI to reflect the player's current bankroll.
        """
        self.bankroll_label.config(text=f"Bankroll: €{self.game.player.bankroll:.2f}")


def main():
    """
    Entry point for the Blackjack GUI application.
    Initializes the Tkinter root window and starts the main event loop.
    """
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
