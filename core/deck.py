import random

class Deck:
    '''
    class Deck to manage the skyjo deck
    '''
    def __init__(self):
        self.deck = self.create_deck()

    
    def create_deck(self):
        '''
        create a new official skyjo deck
        150 cards:
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