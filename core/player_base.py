import random


class SkyjoPlayer:
    def __init__(self, name):
        self.name = name
        self.grid = {}
        self.score = 0

    def init_player(self,deck):
        for row in range(3):
            for col in range(4):
                # Une seule pioche par case
                self.grid[f"carte_{row * 4 + col + 1}"] = {"value": deck.pick_card(), "visible": False}
    
    def compute_score(self):
        self.score = 0
        for card in self.grid.values():
            self.score += card["value"]