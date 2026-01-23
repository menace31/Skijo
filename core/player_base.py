class SkyjoPlayer:
    '''
    Here is the base class for a Skyjo player with attributes name, grid and score.
    '''
    def __init__(self, name):
        self.type_bot="Human"
        self.name = name
        self.grid = {}
        self.score = 0

    def init_player(self,deck):
        '''
        create the player's grid at the beginning of the game by literally picking cards from the deck
        '''
        for row in range(3):
            for col in range(4):
                self.grid[f"carte_{row * 4 + col + 1}"] = {"value": deck.pick_card(), "visible": False, "removed": False}
                if row == 0 and col < 2:
                    self.grid[f"carte_{row * 4 + col + 1}"]["visible"] = True

    def compute_score(self):
        '''
        compute the score of the player, even the hidden cards
        '''
        self.score = 0
        for card in self.grid.values():
            self.score += card["value"]