import cardlib as cl

class Player:
    def __init__(self, name):
        self.name = name
        self.deck: cl.Deck = cl.Deck(0)
    
    def __str__(self):
        return self.name