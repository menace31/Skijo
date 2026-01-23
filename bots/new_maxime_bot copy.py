from core.player_base import SkyjoPlayer
from bots.bot_tools import *
import random

class MaximeBot3(SkyjoPlayer):
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
        grid = public_state["players"][self.name]["grid"]
        max_card = max_card_in_grid(grid)
        equal = equal_card_in_grid(grid, public_state["discard_top"])

        if public_state["discard_top"] < max_card["value"] or equal[1] > 0:
            decison["action"] = "pile"
        else:
            decison["action"] = "deck"
        print(decison)
        return decison
    
    def replace_decision(self, public_state):
        """
        The bot chooses a card from his game to replace with the drawn card or just look at one of his own cards.
        
        :param public_state: the public state of the game

        :return: a dictionary with the keys "action" and "card_name"
        """
        decision = {"action": None, "card_name": None} # action can be "replace" or "look" and card_name is the name of the card to replace or look at
        grid = public_state["players"][self.name]["grid"]
        equal_cards, max_len_equal = equal_card_in_grid(grid, public_state["discard_top"])
        max_equal = None
        max_card = max_card_in_grid(public_state["players"][self.name]["grid"])
        except_values = []
        while equal_card_in_grid(public_state["players"][self.name]["grid"], max_card["value"])[1] > 1:
            except_values.append(max_card["value"])
            max_card = max_card_in_grid(public_state["players"][self.name]["grid"], except_values=except_values)
            print("max_card",max_card)
        if max_len_equal > 0:
            for col_list in equal_cards:
                if len(col_list) == max_len_equal:
                    max_equal = col_list
                    break
            print("bbb")
            decision["action"] = "replace"
            print("max_equal",max_equal)
            idx = int(max_equal[0].split("_")[1])
            for i in [4,8]:
                idx = idx + 4
                if idx > 12:
                    idx -= 12
                if f"carte_{idx}" not in max_equal:
                    break
            print("new_idx",idx)
            target = f"carte_{idx}"
            decision["card_name"] = target
        elif public_state["discard_top"] < max_card["value"]:
            print("aaa")
            decision["action"] = "replace"
            grid = public_state["players"][self.name]["grid"]
            except_values = []
            print(equal_card_in_grid(public_state["players"][self.name]["grid"], max_card["value"]))
            while equal_card_in_grid(public_state["players"][self.name]["grid"], max_card["value"])[1] > 1:
                except_values.append(max_card["value"])
                max_card = max_card_in_grid(public_state["players"][self.name]["grid"], except_values=except_values)
                print("max_card",max_card)
            decision["card_name"] = max_card["name"]
        else:
            decision["action"] = "look"
            name = self.name
            self_grid = public_state["players"][name]["grid"]
            choices = [card for card, data in self_grid.items() if not data.get("removed", False) and not data.get("visible", False)]
            decision["card_name"] = random.choice(choices)
        return decision