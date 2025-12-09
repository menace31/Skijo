# L'IA a besoin de connaître les règles de base
from core.player_base import SkyjoPlayer 

class RandomBot(SkyjoPlayer):
    def __init__(self):
        super().__init__(name="RandomBot")

    def play_turn(self):
        # Implémentez la logique de jeu de l'IA ici
        pass

# L'IA hérite de SkyjoPlayer pour avoir accès aux règles de base du jeu