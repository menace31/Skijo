import random
from . import player_base as pb
from . import deck

class SkyjoBoard:
    def __init__(self):
        self.players = {}
        self.players_order = None
        self.current_player_index = -1
        self.current_player = None
        self.deck = deck.Deck()
        self.discard_pile = []
        self.n_player = None
        self.game_over = False


    def init_game(self, players_name):

        self.n_player = len(players_name)
        self.deck.shuffle_deck()

        for name in players_name:
            self.players[name] = pb.SkyjoPlayer(name)
            self.players[name].init_player(self.deck)
        
        self.discard_pile.append(self.deck.pick_card())
        
        self.players_order = list(self.players.keys())
        self.next_player()

    def pick_from_deck(self):
        # Pioche une carte du deck sans l'ajouter immédiatement à la défausse
        return self.deck.pick_card()
    
    def pick_from_pile(self):
        return self.discard_pile.pop()

    def next_player(self):
        self.current_player_index += 1
        self.current_player = self.players_order[self.current_player_index%self.n_player]

    def get_discard_card(self):
        return self.discard_pile[-1]
    
    def put_discard_card(self,player,card_name):
        self.discard_pile.append(self.players[player].grid[card_name].get("value"))

    # ========== FIN DE PARTIE ==========
    def is_player_all_visible(self):
        for card in self.players[self.current_player].grid.values():
            if not card.get("visible"):
                return False
        return True

    def finalize_if_needed(self):
        """Retourne True si la partie se termine après le tour du joueur."""
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
        self.winner = None if len(winners) > 1 else winners[0]
        self.game_over = True
        return True
