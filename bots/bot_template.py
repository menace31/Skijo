from core.player_base import SkyjoPlayer
import random

class TemplateBot(SkyjoPlayer):
    '''
    Template for future bots.

    exemple of public_satate:
    {
    "current_player": "Riley_bot",
    "discard_top": 6,
    "deck_count": 125,
    "players": {
        "HumanPlayer": {
        "grid": {
            "carte_1": { "visible": true, "value": -1, "removed": false },
            "carte_2": { "visible": true, "value": 0, "removed": false },
            "carte_3": { "visible": true, "value": 12, "removed": false },
            "carte_4": { "visible": false, "value": null, "removed": false },
            "carte_5": { "visible": false, "value": null, "removed": false },
            "carte_6": { "visible": false, "value": null, "removed": false },
            "carte_7": { "visible": false, "value": null, "removed": false },
            "carte_8": { "visible": false, "value": null, "removed": false },
            "carte_9": { "visible": false, "value": null, "removed": false },
            "carte_10": { "visible": false, "value": null, "removed": false },
            "carte_11": { "visible": false, "value": null, "removed": false },
            "carte_12": { "visible": false, "value": null, "removed": false }
        },
        "score": 0
        },
        "Riley_bot": {
        "grid": {
            "carte_1": { "visible": true, "value": 2, "removed": false },
            "carte_2": { "visible": true, "value": 3, "removed": false },
            "carte_3": { "visible": false, "value": null, "removed": false },
            "carte_4": { "visible": false, "value": null, "removed": false },
            "carte_5": { "visible": false, "value": null, "removed": false },
            "carte_6": { "visible": false, "value": null, "removed": false },
            "carte_7": { "visible": false, "value": null, "removed": false },
            "carte_8": { "visible": false, "value": null, "removed": false },
            "carte_9": { "visible": false, "value": null, "removed": false },
            "carte_10": { "visible": false, "value": null, "removed": false },
            "carte_11": { "visible": false, "value": null, "removed": false },
            "carte_12": { "visible": false, "value": null, "removed": false }
        },
        "score": 0
        }
    }
    }
    '''
    random_name = ["Alex_bot", "Max_bot", "Sam_bot", "Jordan_bot", "Taylor_bot", "Casey_bot", "Riley_bot", "Jamie_bot"]
    def __init__(self, name = None):
        if name is None:
            name = random.choice(self.random_name)
        super().__init__(name=name)

    
    def pick_decision(self, public_state):
        '''
        The bot chooses between drawing from the deck or the discard pile.
        
        :param self: just himself
        :param public_state: the public state of the game

        :return: a dictionary with the key "action"
        '''
        decison = {"action": None}  # action can be "deck" or "pile"
        return decison
    
    def replace_decision(self, public_state):
        """
        The bot choose a card from his game ta replace with the drawn card or just look one of his own card.
        
        :param self: Description
        :param public_state: Description

        :return: a dictionary with the keys "action" and "card_name"
        """
        decision = {"action": None, "card_name": None} # action can be "replace" or "look" and card_name is the name of the card to replace or look at like "carte_1"
        return decision
