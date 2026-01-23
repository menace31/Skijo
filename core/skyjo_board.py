import copy
from . import player_base as pb
from . import deck

class SkyjoBoard:
    '''
    Board of the Skyjo game managing players, deck, discard pile and game state.
    This class represent the backend logic of the game and is useful to manage a future development of the GUI on differents plateforms.
    '''
    def __init__(self):
        self.have_human_player = False
        self.players = {}
        self.players_order = None
        self.current_player_index = -1
        self.current_player = None
        self.previous_player = None
        self.deck = deck.Deck()
        self.discard_pile = []
        self.n_player = None
        self.game_over = False


    def init_game(self, players):

        players_name = [player.name for player in players]
        self.n_player = len(players_name)
        self.deck.shuffle_deck()

        for player in players:
            self.players[player.name] = player
            self.players[player.name].init_player(self.deck)

        self.discard_pile.append(self.deck.pick_card())
        
        self.players_order = list(self.players.values())
        self.first_player()

    def first_player(self):
        max_score = -20000
        first_player = None
        for player in self.players.values():
            score = player.grid["carte_1"]["value"] + player.grid["carte_2"]["value"]
            if score > max_score:
                max_score = score
                first_player = player
        self.current_player = first_player
        self.current_player_index = self.players_order.index(first_player)

    def pick_from_deck(self):

        new_card = self.deck.pick_card()
        self.discard_pile.append(new_card)
        return new_card
    
    def pick_from_pile(self):
        return self.discard_pile.pop()

    def next_player(self, ):
        self.current_player_index += 1
        self.previous_player = self.current_player
        self.current_player = self.players_order[self.current_player_index%self.n_player]

    def get_discard_card(self):
        return self.discard_pile[-1]
    
    def put_discard_card(self,player,card_name):
        self.discard_pile.append(self.players[player].grid[card_name].get("value"))

    def get_public_state(self, viewer_name):
        """returns a copy of the public state of the game as seen by the player 'viewer_name'."""
        state = {
            "current_player": self.current_player.name if hasattr(self.current_player, "name") else self.current_player,
            "discard_top": self.discard_pile[-1] if self.discard_pile else None,
            "deck_count": len(self.deck.deck),
            "players": {},
        }

        for name, player in self.players.items():
            grid_view = {}
            for card_name, card in player.grid.items():
                if name == viewer_name:
                    val = card["value"] if card.get("visible") else "hidden"
                else:
                    val = card["value"] if card.get("visible") else "hidden"
                grid_view[card_name] = {
                    "visible": card.get("visible", False),
                    "value": val,
                    "removed": card.get("removed", False),
                }
            state["players"][name] = {
                "grid": grid_view,
                "score": player.score,
            }

        return copy.deepcopy(state)

    def is_player_all_visible(self):
        for card in self.players[self.current_player.name].grid.values():
            if not card.get("visible"):
                return False
        return True

    def finalize_if_needed(self):
        """
        set the game_over variable to True if the game is over and determine the winner if the game_over variable has been set to true previously to let the last player finish his turn
        """
        if self.game_over:
            return True
        if not self.is_player_all_visible():
            return False

        for p in self.players.values():
            p.compute_score()
        scores = {}
        for name in self.players:
            scores[name] = self.players[name].score
        min_score = min(scores.values())
        winners = []
        for name, sc in scores.items():
            if sc == min_score:
                winners.append(name)
        if len(winners) > 1:
            self.winner = None
        else:
            self.winner = winners[0]
        self.game_over = True
