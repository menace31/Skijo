import tkinter as tk
from tkinter import ttk, messagebox



class SkyjoApp:
    """Application principale Skyjo"""
    
    def __init__(self, root: tk.Tk, game, scores):
        """
        Initialise l'application.
        """
        self.scores = scores
        self.root = root
        self.root.title("Skyjo")
        self.game = game
        self.root.geometry("1000x700")
        self.boutons_cardes = {}

        self.is_selected = "nothing"
        self.selected_card = None  # Valeur tirée (deck ou pile) en attente de placement

        self.players_name = list(self.game.players.keys())
        for name in self.players_name[:len(self.players_name)//2]:
            self.create_grid(name)

        self.deck_button = ttk.Button(self.root, text="Piocher une carte", command=self.pick_deck_card)
        self.deck_button.pack(pady=10)

        self.pile_button = ttk.Button(self.root, text=self.game.discard_pile[-1], command=self.click_discard_pile)
        self.pile_button.pack(pady=10)

        for name in self.players_name[len(self.players_name)//2:]:
            self.create_grid(name)

    def create_grid(self, name):
        """Crée une grille de jeu Skyjo."""
        self.grid_frame = ttk.Frame(self.root)
        self.grid_frame.pack(pady=10)

        self.boutons_cardes[name] = {}
        for row in range(3):
            for col in range(4):
                cmd=lambda r=row, c=col: self.on_card_click(name,r, c)
                card_button = ttk.Button(self.grid_frame, name=f"carte_{row * 4 + col + 1}", text="?", command=cmd)
                card_button.grid(row=row, column=col, padx=5, pady=5)
                self.boutons_cardes[name][card_button._name] = card_button

    def on_card_click(self, name, row, col):
        if self.game.current_player == name and self.is_selected != "nothing":
            bouton = self.boutons_cardes[name][f"carte_{row * 4 + col + 1}"]

            if self.is_selected == "deck" and self.selected_card is not None:
                # Placer la carte piochée du deck, envoyer l'ancienne à la défausse
                old_card_name = bouton._name
                self.game.put_discard_card(name, old_card_name)
                bouton.config(text=self.selected_card)
                self.game.players[name].grid[old_card_name] = {"value": self.selected_card, "visible": True}
                self.selected_card = None

            elif self.is_selected == "pile":
                # Prendre la carte du dessus de la défausse, envoyer l'ancienne à la défausse
                carte_value = self.game.pick_from_pile()
                old_card_name = bouton._name
                self.game.put_discard_card(name, old_card_name)
                bouton.config(text=carte_value)
                self.game.players[name].grid[old_card_name] = {"value": carte_value, "visible": True}

            self.update_pile()
            self.check_col(name,row,col)
            self.handle_end_of_turn()
            self.is_selected = "nothing"


    def pick_deck_card(self):
        if self.is_selected == "nothing":
            self.is_selected = "deck"
            self.selected_card = self.game.pick_from_deck()
            # Affiche la carte tirée pour information
            self.pile_button.config(text=self.selected_card)

    def click_discard_pile(self):
        self.is_selected = "pile"

    def update_pile(self):
        self.pile_button.config(text=self.game.get_discard_card())

    def check_col(self,name,row,col):
        # Vérifie si les 3 cartes de la colonne sont identiques
        col_index = col
        card_names = [f"carte_{col_index + 1}", f"carte_{col_index + 5}", f"carte_{col_index + 9}"]
        values = [self.game.players[name].grid[cn]["value"] for cn in card_names]
        if values[0] == values[1] == values[2]:
            self.remove_col(name, col_index + 1)

    def remove_col(self,name,number):
        for i in range(3):
            card_name = f"carte_{(i * 4 + number)}"
            bouton = self.boutons_cardes[name][card_name]
            bouton.destroy()
            self.game.players[name].grid[card_name]["value"] = 0
            self.game.players[name].grid[card_name]["visible"] = True
        self.root.destroy()
    

    def handle_end_of_turn(self):
        # Vérifie fin de partie via moteur
        ended = self.game.finalize_if_needed()
        if ended:
            winners = {}
            for name in self.players_name:
                self.scores[name]["score"] += self.game.players[name].score
                winners[name] = self.scores[name]["score"]
            
            if max(winners.values()) >= 100:
                min_score = min(winners.values())
                for name, sc in winners.items():
                    if sc == min_score:
                        self.scores[name]["win"] += 1
                        for n in self.players_name:
                            self.scores[n]["score"] = 0

            print("Scores finaux :", self.scores)
            self.root.destroy()
        else:
            self.game.next_player()


