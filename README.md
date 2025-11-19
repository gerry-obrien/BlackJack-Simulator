# Blackjack Simulator - Final Version

## Overview
The **Blackjack Simulator** is a Python-based game that allows players to experience the excitement of Blackjack, either through the terminal or a graphical user interface (GUI). This project faithfully implements standard Blackjack rules while adding advanced features such as insurance, splitting, doubling down, and surrendering. It is designed to replicate the feel of a real casino Blackjack game with an intuitive user experience.

This final version includes both terminal and GUI-based gameplay, offering flexibility for players. The project adheres to professional Python project standards, using modular design and object-oriented programming principles.

---

## Features
### Core Gameplay
- **Bankroll Management**:
  - Player starts with €1000.
  - Minimum bet is €10.
- **Dynamic Dealer Logic**:
  - Dealer stands at 17 or higher.
  - Handles soft 17 scenarios (Ace valued as 11 or 1).
- **Flexible Actions**:
  - Hit, Stand, Double Down, Split, Surrender, and Insurance.
- **Advanced Features**:
  - Blackjack pays 3:2.
  - Insurance pays 2:1.
  - Splitting hands into two independent bets.
  - Dynamic Ace handling (value adjusts between 1 and 11 to avoid busting).

### Graphical User Interface (GUI)
- **Dealer and Player Display**:
  - Clear visual representation of cards and totals.
  - Dealer's hidden card reveals dynamically after the player's turn.
- **Action Buttons**:
  - Buttons for Hit, Stand, Double, Surrender, and Split.
- **Bet Input**:
  - Enter your bet using a text box.
- **Interactive Dialogs**:
  - Pop-ups for Blackjack, Insurance, Bust, and Round Results.

    
---

## File Structure
- **`deck.py`**: Manages the deck of cards (creation, shuffling, dealing).
- **`player.py`**: Defines the `Player` class for managing hands and bankroll.
- **`game.py`**: Implements core game logic for Blackjack rules and advanced features.
- **`utils.py`**: Contains helper functions for hand calculations and display.
- **`main.py`**: Implements core game logic for Blackjack rules and advanced features.
- **`gui.py`**: Implements the graphical user interface for the game.
- **`cards/`**: Contains PNG images for card representations.
- **`requirements.txt`**: Lists the required Python packages for the project.

---

## Requirements
The program requires Python 3.7 or higher and the following Python package:
- **Pillow**: For image handling in the GUI.

Install the dependencies using:
```bash
pip install -r requirements.txt
```

---

## How to Run
### For GUI Mode:
1. Clone the repository:
   ```bash
   git clone git@github.com:SachaKsk/Blackjack-Simulator.git
   cd Blackjack-Simulator
   ```

2. Run the GUI:
   ```bash
   python gui.py
   ```

### For Terminal Mode:
1. Run the terminal-based Blackjack:
   ```bash
   python main.py
   ```

---

## Rules
### General
- **Dealer's Cards**: The dealer reveals one card while keeping the other hidden until the player's turn is complete.
- **Objective**: Get a hand value closer to 21 than the dealer without exceeding 21.
- **Card Values**: Number cards are worth their face value, face cards are worth 10, and Aces can be 1 or 11.
- **Gameplay**: Players can Hit, Stand, Double Down, Surrender, or Split (if eligible). The dealer completes their turn after the player.

---

### Actions
#### Hit
- **Description**: Request an additional card to improve your hand.
- **Limitations**: Continues until the player Stands or busts (exceeds 21).

#### Stand
- **Description**: End your turn and keep your current hand.

#### Doubling Down
- **Description**: Double your bet, receive one final card, and end your turn.
- **When to Use**: Often with a strong initial hand (e.g., 9, 10, or 11).

#### Surrender
- **Description**: Forfeit half your bet to end the round early.
- **When to Use**: Usually against a strong dealer upcard (e.g., Ace or 10).

#### Splitting
- **Description**: Divide a pair (e.g., 8-8) into two separate hands with independent bets.
- **Limitations**: Each hand is played independently; additional bets must be placed.

---

### Special Rules
#### Insurance
- **Description**: A side bet (50% of the original bet) when the dealer’s upcard is an Ace.
- **Outcome**:
  - Pays 2:1 if the dealer has Blackjack.
  - Lost if the dealer does not have Blackjack.

---

### Dealer Rules
- **Hitting/Standing**: Dealer hits on 16 or less and stands on 17 or higher (including soft 17).
- **Winning Conditions**: Dealer wins if closer to 21 than the player without busting.


---

## Future Improvements
- Multiplayer support for playing Blackjack with friends.
- Integration of side bets like Perfect Pairs or 21+3.
- Adding animations for card dealing in the GUI.

---

## Contributors
This project was developed by:
- **Sacha Koskas**
- **Gerry O'Brien**
- **Henri Boisson**

---

## Credits
- **Card Images**: The card images in the `cards/` folder were sourced from David Bellot; you can find more at: http://svg-cards.sourceforge.net/

