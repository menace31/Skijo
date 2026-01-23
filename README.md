# Skyjo Bot Competition

Welcome to the Skyjo Bot Competition! This repository hosts a Python implementation of the Skyjo card game with a focus on bot development and fair competition.

## Table of Contents
- [Game Overview](#game-overview)
- [Bot Competition Rules](#bot-competition-rules)
- [Creating Your Bot](#creating-your-bot)
- [Public State Information](#public-state-information)
- [Bot API Reference](#bot-api-reference)
- [Anti-Cheat System](#anti-cheat-system)
- [Submission Guidelines](#submission-guidelines)

## Game Overview

Skyjo is a card game where players aim to have the lowest score by managing a grid of 12 cards (3 rows × 4 columns). The game ends when one player reveals all their cards, and the player with the lowest total score wins.

### Basic Rules
- Each card has a value from -2 to 12
- Players can draw from the deck or take the top card from the discard pile
- When you draw, you can either replace a card in your grid or look at one of your hidden cards
- If a column has 3 identical cards, that column is removed (scoring 0)
- The game ends when all cards of one player are revealed

## Bot Competition Rules

### Competition Format
1. **Fair Play**: All bots must use only the information provided through the `public_state` variable
2. **No Cheating**: Bots cannot access the game object, other players' hidden cards, or the deck contents
3. **Deterministic or Random**: Your bot can use any strategy, from simple random choices to complex AI algorithms
4. **Time Limits**: Each decision must be made within a reasonable time frame (no infinite loops)
5. **Error Handling**: Invalid decisions will raise an error and disqualify the bot from that game

### Scoring System
- Games are played in a best-of-3 format
- The bot with the lowest cumulative score across games wins
- If a score reaches 100+, the player with the lowest score gets a win point

## Creating Your Bot

### Step 1: Use the Template

Start with the `bots/bot_template.py` file as your base:

```python
from core.player_base import SkyjoPlayer
import random

class MyCustomBot(SkyjoPlayer):
    '''
    Description of your bot's strategy.
    '''
    def __init__(self, name="MyBot"):
        super().__init__(name=name)
    
    def pick_decision(self, public_state):
        '''
        Decide whether to draw from the deck or take from the discard pile.
        
        :param public_state: Dictionary containing all visible game information
        :return: Dictionary with key "action" - value must be "deck" or "pile"
        '''
        decision = {"action": None}
        # Your logic here
        decision["action"] = "deck"  # or "pile"
        return decision
    
    def replace_decision(self, public_state):
        """
        Decide which card to replace or look at after drawing.
        
        :param public_state: Dictionary containing all visible game information
        :return: Dictionary with keys "action" and "card_name"
                 - action: "replace" or "look"
                 - card_name: "carte_1" through "carte_12"
        """
        decision = {"action": None, "card_name": None}
        # Your logic here
        decision["action"] = "replace"  # or "look"
        decision["card_name"] = "carte_1"  # Choose any valid card
        return decision
```

### Step 2: Implement Your Strategy

Your bot must implement two methods:

#### 1. `pick_decision(public_state)`
This method is called when it's your turn to draw a card.

**Return format:**
```python
{"action": "deck"}  # Draw from the deck
# OR
{"action": "pile"}  # Take from the discard pile
```

**Strategy considerations:**
- If the discard pile has a low value card, it might be worth taking
- Drawing from the deck gives you the option to just "look" at one of your hidden cards
- Consider the visible cards in your grid and opponents' grids

#### 2. `replace_decision(public_state)`
This method is called after you've drawn a card to decide what to do with it.

**Return format:**
```python
{"action": "replace", "card_name": "carte_5"}  # Replace card 5 with drawn card
# OR
{"action": "look", "card_name": "carte_8"}  # Look at hidden card 8
```

**Strategy considerations:**
- If you drew a high value card, you might want to replace a high value visible card
- If you drew from the deck, you can choose to "look" at one of your hidden cards instead
- Card names are "carte_1" through "carte_12" (grid positions left-to-right, top-to-bottom)
- You can only "look" at cards that are not yet visible
- You cannot interact with cards that have been removed (from column removal)

### Step 3: Test Your Bot

Run your bot against the RandomBot to test:

```python
from bots.your_bot import YourBot
from bots.random_bot import RandomBot

player_1 = YourBot("YourBot")
player_2 = RandomBot("RandomBot")
```

## Public State Information

Your bot receives a `public_state` dictionary containing only visible and public information:

### Public State Structure

```python
{
    "current_player": "PlayerName",  # Name of the current player
    "discard_top": 5,                # Value of the top card on discard pile
    "deck_count": 120,               # Number of cards remaining in deck
    "players": {
        "PlayerName": {
            "score": 15,             # Current score (only computed at game end)
            "grid": {
                "carte_1": {
                    "visible": True,
                    "value": 5,      # Only visible if "visible" is True
                    "removed": False
                },
                "carte_2": {
                    "visible": False,
                    "value": None,   # Hidden cards show None
                    "removed": False
                },
                # ... carte_3 through carte_12
            }
        },
        "OpponentName": {
            # Same structure for all players
        }
    }
}
```

### Available Information

✅ **You CAN see:**
- Your own visible cards (value and position)
- All opponents' visible cards (value and position)
- Which cards are hidden (but not their values)
- Which cards have been removed (column removal)
- The top card of the discard pile
- How many cards remain in the deck
- Current player's turn

❌ **You CANNOT see:**
- Hidden card values (yours or opponents')
- Cards in the deck
- Future draws
- Internal game state variables

### Filtering Valid Choices

When selecting a card, make sure to filter out invalid options:

```python
# Get your own grid
my_grid = public_state["players"][self.name]["grid"]

# For "look" action - only hidden, non-removed cards
hidden_cards = [
    card for card, data in my_grid.items()
    if not data["visible"] and not data["removed"]
]

# For "replace" action - only non-removed cards
replaceable_cards = [
    card for card, data in my_grid.items()
    if not data["removed"]
]
```

## Bot API Reference

### Required Methods

#### `__init__(self, name=None)`
- Initialize your bot with a unique name
- Must call `super().__init__(name=name)`

#### `pick_decision(self, public_state) -> dict`
- **Called**: At the start of your turn
- **Parameter**: `public_state` - Dictionary with visible game information
- **Returns**: `{"action": "deck"}` or `{"action": "pile"}`
- **Raises**: `ValueError` if return format is invalid

#### `replace_decision(self, public_state) -> dict`
- **Called**: After drawing a card
- **Parameter**: `public_state` - Dictionary with updated game information
- **Returns**: `{"action": "replace"|"look", "card_name": "carte_X"}`
- **Raises**: `ValueError` if return format is invalid or card is invalid

### Inherited Attributes

From `SkyjoPlayer` base class:
- `self.name` - Your bot's name
- `self.grid` - Your card grid (but use `public_state` instead for fair play!)
- `self.score` - Your current score

⚠️ **Important**: Do not access `self.grid` directly in competition mode. Use only `public_state` to ensure fair play.

## Anti-Cheat System

The competition uses several anti-cheat mechanisms:

### 1. Public State API
- Bots receive a **deep copy** of the public state
- Hidden cards are replaced with `None` values
- Direct access to game objects is blocked

### 2. Decision Validation
- All bot decisions are validated before execution
- Invalid card selections raise errors
- Invalid action types raise errors

### 3. Error Handling
```python
# Invalid decision examples that will raise errors:

# Wrong action type
{"action": "take"}  # ❌ Must be "deck" or "pile"

# Invalid card name
{"action": "replace", "card_name": "carte_15"}  # ❌ Only 1-12 exist

# Trying to interact with removed card
{"action": "look", "card_name": "carte_3"}  # ❌ If carte_3 was removed

# Trying to look at visible card
{"action": "look", "card_name": "carte_1"}  # ❌ If carte_1 is already visible
```

## Submission Guidelines

### File Structure
```
bots/
├── your_bot_name.py    # Your bot implementation
└── __init__.py         # Leave as is
```

### Naming Conventions
- Class name: `YourBotNameBot` (e.g., `SmartStrategyBot`)
- File name: `your_bot_name.py` (e.g., `smart_strategy_bot.py`)
- Bot name: Any unique string (set in `__init__`)

### Testing Checklist
Before submitting, ensure:
- [ ] Your bot inherits from `SkyjoPlayer`
- [ ] Both `pick_decision()` and `replace_decision()` are implemented
- [ ] Return values match the required format exactly
- [ ] Your bot only uses `public_state` information
- [ ] Your bot handles edge cases (e.g., all cards visible)
- [ ] No infinite loops or excessive computation time
- [ ] Your bot doesn't crash on invalid states

### Example Submission
See `bots/random_bot.py` for a complete working example of a valid bot implementation.

## Running the Competition

To run a competition match:

```python
from main import main
from bots.your_bot import YourBot
from bots.opponent_bot import OpponentBot

player_1 = YourBot("YourBot")
player_2 = OpponentBot("OpponentBot")
players = [player_1, player_2]

scores = {
    player_1.name: {"win": 0, "score": 0},
    player_2.name: {"win": 0, "score": 0}
}

# Best of 3
while scores[player_1.name]["win"] < 3 and scores[player_2.name]["win"] < 3:
    main(players, scores)

print("Final Results:", scores)
```

## Good Luck!

May the best bot win! Remember: creativity, strategy, and clean code are all valued in this competition.

For questions or issues, please open an issue in the repository.
