from gui.skyjoApp import SkyjoApp
from gui.skyjoApp_gui import SkyjoApp_gui
from bots.random_bot import RandomBot
from bots.maxime_bot import MaximeBot
from bots import *
from core.skyjo_board import SkyjoBoard
from core.player_base import SkyjoPlayer
import core.player_base as pb
import tkinter as tk
import importlib
import inspect
from pathlib import Path

def load_bot_classes(directory_name="bots"):
    bot_classes = {}
    path = Path(directory_name)

    for file_path in path.glob("*.py"):
        module_name = f"{directory_name}.{file_path.stem}"
        module = importlib.import_module(module_name)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module_name:
                bot_classes[name] = obj
                print(f"Classe chargée : {name} depuis {module_name}")

    return bot_classes

bots_classes = load_bot_classes()


def main(players,scores, have_human_player=True):
    game = SkyjoBoard()
    game.init_game(players)
    if have_human_player:
        root = tk.Tk()
        SkyjoApp_gui(root, game,scores)
        root.mainloop()
    else:
        SkyjoApp(None, game,scores)

if __name__ == "__main__":
    player_1 = SkyjoPlayer("Maxime") 
    #player_1 = bots_classes["MaximeBot2"]("random_bot_1")
    player_2 = bots_classes["MaximeBot3"]("maxime_bot_1")
    players = [player_1, player_2]
    scores = {}
    for player in players:
        scores[player.name] = {"win": 0, "score": 0}

    if player_1.type_bot=="Human" or player_2.type_bot=="Human":
        while scores[player_1.name]["win"] + scores[player_2.name]["win"] < 1:
            main(players,scores)
    else:
        win_condition = 100
        while scores[player_1.name]["win"] + scores[player_2.name]["win"] < win_condition:
            main(players,scores, have_human_player=False)
    
        print(f"\n\nFinal scores after {win_condition} wins:")
        print(f"{player_1.name}: {scores[player_1.name]['win']} wins, {player_2.name}: {scores[player_2.name]['win']} wins")