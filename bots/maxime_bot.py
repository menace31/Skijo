from core.player_base import SkyjoPlayer
from bots.bot_tools import *
import random

class MaximeBot(SkyjoPlayer):
    '''
    A bot that doesn't take account of the game and just plays randomly
    '''
    random_name = ["Alex_bot", "Max_bot", "Sam_bot", "Jordan_bot", "Taylor_bot", "Casey_bot", "Riley_bot", "Jamie_bot"]
    def __init__(self, name = None):
        if name is None:
            name = random.choice(self.random_name)
        super().__init__(name=name)
        self.type_bot="Bot"

    
    def pick_decision(self, public_state):
        '''
        The bot chooses between drawing from the deck or the discard pile.
        
        :param public_state: the public state of the game

        :return: a dictionary with the key "action"
        '''
        decison = {"action": None}  # action can be "deck" or "pile"
        if public_state["discard_top"] <= 4:
            decison["action"] = "pile"
        else:
            decison["action"] = "deck"
        return decison
    
    def replace_decision(self, public_state):
        """
        The bot chooses a card from his game to replace with the drawn card or just look at one of his own cards.
        
        :param public_state: the public state of the game

        :return: a dictionary with the keys "action" and "card_name"
        """
        decision = {"action": None, "card_name": None} # action can be "replace" or "look" and card_name is the name of the card to replace or look at
        
        decision["action"] = random.choice(["replace", "look"])
        name = self.name
        self_grid = public_state["players"][name]["grid"]
        if decision["action"] == "look":
            choices = [card for card, data in self_grid.items() if not data.get("removed", False) and not data.get("visible", False)]
        else:
            choices = [card for card, data in self_grid.items() if not data.get("removed", False) and not data.get("visible", False)]
        if not choices:
            return None
        decision["card_name"] = random.choice(choices)
        return decision