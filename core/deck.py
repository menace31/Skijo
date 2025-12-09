import random

class Deck:

    def __init__(self):
        self.deck = self.creat_deck()

    
    def creat_deck(self):
        '''
        creat a new deck
        '''
        sorted_deck = []
        for i in range(-2,13):
            for j in range(5):
                sorted_deck.append(i)
        for i in range(-1,13):
            for j in range(5):
                sorted_deck.append(i)
        for j in range(5):
            sorted_deck.append(0)
        
        return sorted_deck
    
    def shuffle_deck(self):
        '''
        shuffle the deck
        '''
        random.shuffle(self.deck)

    def pick_card(self):
        '''
        pick a card from the deck
        '''
        return self.deck.pop()