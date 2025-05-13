from math import floor
import random

# Private variables
__full_text_keys = [
    'A',
    'J',
    'Q',
    'K',
    '-',
    'C',
    'D',
    'H',
    'S',
]
__full_text_values = [
    "Ace",
    "Jack",
    "Queen",
    "King",
    " of ",
    "Clubs",
    "Diamonds",
    "Hearts",
    "Spades",
]
__pretty_values = [
    'A',
    'J',
    'Q',
    'K',
    '',
    '♣',
    '♦',
    '♥',
    '♠'
]

class Deck:
    """
    A class representing any number of decks of cards

    (Constructor)
    num (int): Number of 52-card decks to include in this deck
    """
    @staticmethod
    def new(num: int = 1) -> list[str]:
        """
        Generates a deck of cards, containing a user-specified amount of decks

        num (int): Number of decks to include
        """
        suits = ['C', 'D', 'H', 'S']
        out: list[str] = []
        while num > 0:
            for suit in suits:
                for i in range(1, 14):
                    match i:
                        # Ace
                        case 1:
                            out.append("A")
                        # Jack
                        case 11:
                            out.append("J")
                        # Queen
                        case 12:
                            out.append("Q")
                        # King
                        case 13:
                            out.append("K")
                        # Anything else
                        case _:
                            out.append(str(i))

                    out[-1] += "-" + suit

            num -= 1

        return out
    
    def shuffle(self):
        """
        Randomly shuffles the Deck using the Fisher-Yates algorithm
        """
        self.cards = shuffle_deck_fisher_yates(self.cards)
    
    def draw(self, num: int = 1) -> list[str] | str:
        """
        Draws a card from the Deck, removing it from the Deck and returning it

        num (int): How many cards to draw
        """
        out = []

        while num > 0:
            card = self.cards[-1]
            out.append(card)
            del self.cards[-1]
            num -= 1
        
        return out if len(out) > 1 else out[0]

    def clear(self):
        """
        Clears the deck
        """
        self.cards.clear()
    
    def __add__(self, other):
        if isinstance(other, Deck):
            new = Deck(0)
            new.cards += self.cards + other.cards
            return new
        elif isinstance(other, list) and all(isinstance(item, str) for item in other):
            for string in other:
                if not validate_card(string):
                    raise ValueError("Card does not match expected format")
                
            
            new = Deck(0)
            new.cards += self.cards + other
            return new
        elif isinstance(other, str):
            if not validate_card(other):
                raise ValueError("Card does not match expected format")

            new = Deck(0)
            self.cards.append(other)
            new.cards += self.cards
            return new

    # Report len() of class as number of cards in deck
    def __len__(self):
        return len(self.cards)

    # Allow indexing over class to get cards
    def __getitem__(self, index):
        return self.cards[index]

    # Allow running .contains() on Deck    
    def __contains__(self, card):
        return card in self.cards

    # Allow iterating over Deck
    def __iter__(self):
        return iter(self.cards)

    # Allow pretty printing Deck
    def __str__(self):
        return " ".join(
            [pretty_print_card(card) for card in self.cards]
        )

    # Creates a new instance of Deck
    def __init__(self, num: int = 1):
        self.cards = Deck.new(num)

# This is the same shuffling algorithm that random.shuffle() uses
# noinspection PyTypeChecker
def shuffle_deck_fisher_yates(deck: list[str]) -> list[str]:
    """
    Shuffles a deck with the Fisher-Yates algorithm, which works in place
    Then returns the deck just incase

    deck (list[str]): Deck to shuffle
    """
    len_deck = len(deck)
    while len_deck > 1:
        i = int(floor(random.random() * len_deck))
        len_deck -= 1
        deck[i], deck[len_deck] = deck[len_deck], deck[i]
    
    return deck

def shuffle_deck_riffle(deck: list[str]) -> list[str]:
    """
    Shuffles a deck with a Riffle shuffle and returns the shuffled deck

    deck (list[str]): Deck to shuffle
    """

    cut = len(deck) // 2
    deck, second_deck = deck[:cut], deck[cut:]
    for i, el in enumerate(second_deck):
        insert_i = i * 2 + 1
        deck.insert(insert_i, el)
    
    return deck
    


def get_card_full_text(card: str) -> str | None:
    """
    Function for pretty printing a card from a Deck

    card (str): card to pretty print
    """
    if not validate_card(card):
        return None

    for k, v in zip(__full_text_keys, __full_text_values):
        card = card.replace(k, v)

    return card

def pretty_print_card(card: str) -> str | None:
    """
    Prints a card's number immediately followed by a symbol representing the suit

    card (str): Card to pretty print
    """
    if not validate_card(card):
        return None

    for k, v in zip(__full_text_keys, __pretty_values):
        card = card.replace(k, v)

    return card

def validate_card(string: str) -> bool:
    """
    Verifies that a card follows the string format for cards
    Cards follow this format, where:
        V = Value
        S = Suit
        "V-S"

    card (str): card to validate
    """
    if len(string) != 3 and len(string) != 4:
        return False

    if '-' not in string:
        return False

    split = string.split('-')

    match split[0]:
        case sub if sub.isnumeric() and int(sub) in range(2, 11):
            pass
        case 'A' | 'J' | 'Q' | 'K':
            pass
        case _:
            return False
    
    match split[1]:
        case 'C' | 'D' | 'H' | 'S':
            pass
        case _:
            print(string[2])
            return False
    
    return True