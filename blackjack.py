import cardlib as cl
import copy
from enum import Enum
import player
from helpers import center_many, clear, confirm, input_num
import time

class Action(Enum):
    INVALID = -1
    HIT = 1
    STAND = 2
    QUIT = 3

class Player(player.Player):
    """
    Special version of playing with standing: bool in it
    """
    def __init__(self, name):
        super().__init__(name)
        self.standing = False


class Blackjack:
    """
    Represents and manages a game of blackjack

    Instructions for use:
    game = Blackjack()
    game.play()
    """
    # Public methods
    # Static methods

    @staticmethod
    def get_value_of_card(card: str) -> int:
        """
        Get value of single card

        This isn't used often since it's missing the context of the rest of the deck, for deciding if aces should be 1 or 11
        """
        if not cl.validate_card(card):
            raise ValueError

        try:
            split = card.split('-')
            return int(split[0])
        except ValueError:
            match card[0]:
                case 'A':
                    return 11
                case 'J' | 'Q' | 'K':
                    return 10
                case _:
                    raise ValueError

    @staticmethod
    def get_value_of_deck_list(deck: list[str]) -> int:
        """
        Gets the total value of a deck in list form
        """
        values = [Blackjack.get_value_of_card(card) for card in deck]
        while sum(values) > 21 and 11 in values:
            i = values.index(11)
            values[i] = 1

        return sum(values)

    @staticmethod
    def get_value_of_deck(deck: cl.Deck) -> int:
        """
        Gets the total value of a deck in Deck form
        """
        return Blackjack.get_value_of_deck_list(deck.cards)

    # Award for most unfortunate function names goes to the next two functions
    @staticmethod
    def get_hard_value_of_deck(deck: cl.Deck) -> int:
        """
        Gets the value of a deck with all aces counted as 11
        """

        # Get values of every card in deck
        values = [Blackjack.get_value_of_card(card) for card in deck]
        # Replace all 1s with 11s in deck
        values[:] = [x if x != 1 else 11 for x in values]

        return sum(values)

    @staticmethod
    def get_soft_value_of_deck(deck: cl.Deck) -> int:
        """
        Gets the total value of a deck with all aces counted as 1
        """

        # Get values of every card in deck
        values = [Blackjack.get_value_of_card(card) for card in deck]
        # Replace all 11s with 1s in deck
        values[:] = [x if x != 11 else 1 for x in values]

        return sum(values)

    # Non-static methods
    def play(self):
        """
        Starts the game
        """
        while True:
            for p in self.players.values():
                # Cleanup for (potential) last round
                p.standing = False

                # Clear player decks, adding their cards back into the master deck
                if len(p.deck) > 0:
                    self.deck += p.deck
                    p.deck.clear()

            # Shuffle the deck using Fisher-Yates            
            self.deck.shuffle()

            # Deal each player 2 cards
            self.__initial_deal()

            # Do a round
            if not self.__do_round():
                return

            if any([self.get_value_of_deck(p.deck) <= 21 for p in self.players.values() if p.name != "Dealer"]):
                dealer = self.players["dealer"]
                while self.get_value_of_deck(dealer.deck) < 17:
                    self.__hit(dealer, False)

            clear()
            self.__draw_table(False)
            values = [self.get_value_of_deck(p.deck) for p in self.players.values()]

            if all([value > 21 for value in values]):
                end_game_str = "Everyone BUSTs"
            elif all([value == 21 for value in values]):
                end_game_str = "Everyone DRAWs"
            else:
                temp = [v for v in copy.deepcopy(values) if v <= 21]
                max_value = max(temp)

                if all([value == max_value for value in values]):
                    end_game_str = f"Everyone DRAWs on {values[0]}"
                else:
                    drawn_players_i = [value == max_value for value in values]
                    drawn_players = []
                    if len([p for p in drawn_players_i if p]) > 1:
                        i = 0
                        while i < len(drawn_players_i):
                            if drawn_players_i[i]:
                                drawn_players.append(list(self.players.values())[i].name)

                            i += 1

                        end_game_str = " & ".join(drawn_players) + f" DRAW on {max_value}"
                    else:
                        winner = [p for p in self.players.values() if self.get_value_of_deck(p.deck) == max_value][0]
                        end_game_str = f"{winner.name} WINS"


            print('\n' + end_game_str)
            time.sleep(1)
            res = confirm("\nPlay again?")
            if not res:
                return

    # Private methods
    # Static methods
    @staticmethod
    def __get_num_decks() -> int:
        return input_num("\nHow many decks should be included for this game?\n", bounds=range(1, 1001))

    @staticmethod
    def __get_num_players() -> int:
        return input_num("How many players? [1 to 4]\n", bounds=range(1, 5))

    @staticmethod
    def __read_action():
        res = input("\n1: (H)it\n2: (S)tand\n3: (Q)uit\n").lower()
        if res.isnumeric() and int(res) in range(4):
            return Action(int(res))
        if "hit".startswith(res):
            return Action.HIT

        if "stand".startswith(res):
            return Action.STAND

        if "quit".startswith(res):
            return Action.QUIT

        return Action.INVALID

    # Non-static methods
    def __hit(self, p: Player, hide_dealer: bool = True):
        # Clear screen and redraw table
        clear()
        self.__draw_table(hide_dealer)

        # Draw card and show it, with delay to add tension
        print(f"{p.name} draws...")
        card = self.deck.draw()
        time.sleep(1)
        print(cl.get_card_full_text(card))
        time.sleep(1)

        # Add card to the player's deck
        p.deck += card

    def __draw_player(self, p: Player, hide_dealer: bool = True):
        """
        Draws a player's deck

        p (Player): Player to draw
        hide_dealer (bool): Hide the dealer's first card and total value
        """

        split = str(p.deck).split(" ")

        # Handle hiding dealer
        if hide_dealer and p.name == "Dealer":
            split[0] = "??"

        spacing = "  ".join(split).center(30)

        # Soft value
        svalue = self.get_soft_value_of_deck(p.deck)

        # Hard value
        hvalue = self.get_hard_value_of_deck(p.deck)

        if hide_dealer and p.name == "Dealer":
            value_str = "??"
        elif svalue > 21:
            value_str = "BUST"
        elif svalue == 21:
            value_str = "BLACKJACK"
        else:
            value_str = str(svalue)

        # Handle ace soft values
        if hvalue != svalue and hvalue <= 21:
            if p.name != "Dealer" or not hide_dealer:
                value_str += "/" + str(hvalue)

        value_str = value_str.center(30)
        print(f"{p.name.center(30)}\n{spacing}\n{value_str}")

    def __draw_table(self, hide_dealer: bool = True):
        """
        Draws the table

        hide_dealer (bool): Hide dealer first card and total value
        """
        for _, p in self.players.items():
            self.__draw_player(p, hide_dealer)
            print()

        print("DEALER MUST HIT SOFT 17".center(30) + "\n")

    def __do_round(self):
        for current_player in self.players.values():
            # Handle dealer getting 21, mostly for straight out of the gate 21s
            if current_player.name == "Dealer" and self.get_value_of_deck(current_player.deck) == 21:
                return True

            while self.get_value_of_deck(current_player.deck) < 21 and not current_player.standing:
                if current_player.name == "Dealer":
                    # Skip dealer's turn and set them as standing since they're not controlled by a person
                    current_player.standing = True
                    continue
                
                # Cleanup
                action = Action.INVALID
                while action == Action.INVALID:
                    # Clear screen and draw table and other important elements
                    clear()
                    self.__draw_table()
                    print(center_many("Current Player", current_player.name))

                    # Get current player's next action
                    action = self.__read_action()

                match action:
                    case Action.QUIT:
                        return False
                    case Action.HIT:
                        self.__hit(current_player)
                    case Action.STAND:
                        current_player.standing = True

        return True

    def __get_player_names(self, num: int):
        """
        Get player names
        """
        i = 0
        while i < num:
            name = input(f"\nPlease enter the name of player {i + 1}\n")
            if name.lower() in [p.name.lower() for p in self.players.values()]:
                print("\nName is already in players list, please try another name.")
                continue

            if len(name) > 11:
                print("\nPlease enter a name with less than 11 characters.")
                continue

            self.players[name] = Player(name)

            i += 1

    def __initial_deal(self):
        for p in self.players:
            cards = self.deck.draw(2)
            self.players[p].deck += cards

    # Constructor
    def __init__(self):
        players = Blackjack.__get_num_players()

        # Add in dealer
        self.players: dict[str, Player] = {
            "dealer": Player("Dealer")
        }

        self.__get_player_names(players)

        decks = Blackjack.__get_num_decks()
        self.deck = cl.Deck(decks)
        self.deck.shuffle()