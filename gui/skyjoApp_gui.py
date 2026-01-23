import tkinter as tk
from tkinter import ttk
from bots.random_bot import RandomBot
from PIL import Image, ImageTk
import time


class SkyjoApp_gui:
    """Main application class for the Skyjo game GUI."""
    
    def __init__(self, root: tk.Tk, game, scores):
        """
        Initializes the Skyjo application GUI.
        """
        self.scores = scores
        self.root = root
        self.root.title("Skyjo")
        self.game = game
        self.root.geometry("700x1200")
        self.boutons_cardes = {}

        self.is_selected = "nothing"
        self.selected_card = None

        self.card_images = {}

        for i in range(-2, 13):
            self.card_images[i] = self.import_image(f"assets/cards/{i}.png", (80, 120))
        
        self.card_images["?"] = self.import_image("assets/cards/card_back.png", (80, 120))

        self.players_name = list(self.game.players.keys())
        for name in self.players_name[:len(self.players_name)//2]:
            self.create_grid(name)

        controls_frame = ttk.Frame(self.root)
        controls_frame.pack(pady=100)

        self.deck_button = ttk.Button(controls_frame, image=self.card_images["?"], command=self.pick_deck_card)
        self.deck_button.pack(side="left", padx=5)

        self.pile_button = ttk.Button(controls_frame, image=self.card_images[self.game.discard_pile[-1]], command=self.click_discard_pile)
        self.pile_button.pack(side="left", padx=5)

        for name in self.players_name[len(self.players_name)//2:]:
            self.create_grid(name)
        
        self.bot_play_turn()

    def import_image(self, path, size):
        card_image = Image.open(path)
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.LANCZOS
        card_image = card_image.resize(size, resample)
        return ImageTk.PhotoImage(card_image)
    
    def create_grid(self, name):
        """Create the GUI grid for each player."""
        self.grid_frame = ttk.Frame(self.root)
        self.grid_frame.pack(pady=10)

        self.boutons_cardes[name] = {}
        for row in range(3):
            for col in range(4):
                cmd=lambda r=row, c=col: self.on_card_click(name,r, c)
                card_button = ttk.Button(self.grid_frame, name=f"carte_{row * 4 + col + 1}", command=cmd)
                card_button.config(image=self.card_images["?"])
                if row == 0 and col < 2:
                    card_button.config(image=self.card_images[self.game.players[name].grid[card_button._name]["value"]])
                    self.game.players[name].grid[card_button._name]["visible"] = True
                card_button.grid(row=row, column=col, padx=5, pady=5)
                self.boutons_cardes[name][card_button._name] = card_button

    def on_card_click(self, name, row, col, is_bot=False):
        if self.game.current_player.name == name and self.is_selected != "nothing":
            bouton = self.boutons_cardes[name].get(f"carte_{row * 4 + col + 1}")
            old_card_name = f"carte_{row * 4 + col + 1}"
            if bouton is None:
                return

            if self.is_selected == "pile":
                # Prendre la carte du dessus de la défausse, envoyer l'ancienne à la défausse
                carte_value = self.game.pick_from_pile()
                
                self.game.put_discard_card(name, old_card_name)
                bouton.config(image=self.card_images[carte_value])
                self.game.players[name].grid[old_card_name] = {"value": carte_value, "visible": True, "removed": False}

            elif self.is_selected == "deck":
                if self.game.players[name].grid[old_card_name]["visible"]:
                    raise ValueError("Error: The card to observe is already visible.")
                selected_card = self.game.players[name].grid[old_card_name]["value"]
                bouton.config(image=self.card_images[selected_card])
                self.game.players[name].grid[old_card_name]["visible"] = True
                self.selected_card = None

            self.update_pile()
            self.check_col(name,row,col)
            self.is_selected = "nothing"
            self.handle_end_of_turn()


    def pick_deck_card(self):
        if self.is_selected != "deck":
            self.is_selected = "deck"
            selected_card = self.game.pick_from_deck()
            # Affiche la carte tirée pour information
            self.pile_button.config(image=self.card_images[selected_card])

    def click_discard_pile(self):
        self.is_selected = "pile"

    def update_pile(self):
        self.pile_button.config(image=self.card_images[self.game.get_discard_card()])

    def check_col(self,name,row,col):
        # Check if the 3 cards in the column are identical
        col_index = col
        card_names = [f"carte_{col_index + 1}", f"carte_{col_index + 5}", f"carte_{col_index + 9}"]
        values = []
        for cn in card_names:
            if self.game.players[name].grid[cn]["visible"] is False:
                return

            values.append(self.game.players[name].grid[cn]["value"])

        if values[0] == values[1] == values[2]:
            self.remove_col(name, col_index + 1)

    def remove_col(self,name,number):
        for i in range(3):
            card_name = f"carte_{(i * 4 + number)}"
            bouton = self.boutons_cardes[name].get(card_name)
            if bouton:
                bouton.destroy()
            self.game.players[name].grid[card_name]["value"] = 0
            self.game.players[name].grid[card_name]["visible"] = True
            self.game.players[name].grid[card_name]["removed"] = True
    

    def handle_end_of_turn(self):
        '''
        Check the end of turn and manage end of game if needed.
        '''
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

            print("Final scores:", self.scores)
            self.root.destroy()
        else:
            self.game.next_player()
            self.waiting()
        
    def waiting(self):
        self.root.after(1000, lambda: self.bot_play_turn())
            
    
    def bot_play_turn(self):
        current_player = self.game.current_player
        if current_player and current_player.type_bot == "Bot":
                
                public_state = self.game.get_public_state(current_player.name)
                decision = current_player.pick_decision(public_state)
                if decision["action"] == "deck":
                    self.pick_deck_card()
                elif decision["action"] == "pile":
                    self.click_discard_pile()
                else:
                    raise ValueError(f"Invalid decision from bot {current_player.name} in function \"pick_decision(public_state)\": expected 'deck' or 'pile'. Given value: {decision['action']}")
                
                public_state = self.game.get_public_state(current_player.name)
                decision = current_player.replace_decision(public_state)
                if decision is not None:
                    if decision["card_name"].split("_")[0]=="carte" is False:
                        raise ValueError(f"Invalid decision from bot {current_player.name} in function \"replace_decision(public_state)\": card to replace is not valid. Given value: {decision['card_name']}, expected format 'carte_X' where X is an integer between 1 and 12.")
                    if int(decision["card_name"].split("_")[1]) <= 0 or int(decision["card_name"].split("_")[1]) > 12:
                        raise ValueError(f"Invalid decision from bot {current_player.name} in function \"replace_decision(public_state)\": card to replace is out of range. Given value: {decision['card_name']}")
                    if decision["action"] == "replace":
                        self.click_discard_pile()
                    elif decision["action"] != "look":
                        raise ValueError(f"Invalid decision from bot {current_player.name} in function \"replace_decision(public_state)\": expected 'look' or 'replace'. Given value: {decision['action']}")
                    decision = decision["card_name"]
                    row = (int(decision.split("_")[1]) - 1) // 4
                    col = (int(decision.split("_")[1]) - 1) % 4
                    self.on_card_click(current_player.name, row, col, is_bot=True)
                
                else:
                    raise ValueError(f"Invalid decision from bot {current_player.name} in function \"replace_decision(public_state)\": card to replace is None")