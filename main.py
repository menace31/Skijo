from gui.skyjoApp import SkyjoApp
from bots.random_bot import RandomBot
from core.skyjo_board import SkyjoBoard
import core.player_base as pb
import tkinter as tk


def main(players,scores):

    root = tk.Tk()
    ia_joueur = RandomBot()
    game = SkyjoBoard()
    game.init_game(players)

    app = SkyjoApp(root, game,scores)

    root.mainloop()

if __name__ == "__main__":
    players = ["Maxime", "Antoine"]
    scores = {}
    for name in players:
        scores[name] = {"win": 0, "score": 0}

    while scores["Maxime"]["win"] < 3 and scores["Antoine"]["win"] < 3:
        main(players,scores)