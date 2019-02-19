from pprint import pprint as pp
import random
import sysinfo


# if sysinfo.NO_COLOR == True:

sysinfo.NO_COLOR
sysinfo.WATER
sysinfo.SUNK
sysinfo.HIT


class Ship(object):

    _length = 0 # Length of ship
    name = "" # Name of ship
    coords = []
    def __init__(self):
        assert self._length > 0 and self.name, "Must subclass with length and name!"

        self.hits = 0
        self.coords = []

    def is_sunk(self):
        # Is the ship sunk?

        return self.hits == self._length

    def place(self, col, row, direction):

        if direction == "H":
            self.coords = [(c, row) for c in range(col, col + self._length)]

        elif direction == "V":
            self.coords = [(col, r) for r in range(row, row + self._length)]

        else:
            raise ValueError("Illegal direction")

class AircraftCarrier(Ship):
    _length = 4
    name = "Aircraft Carrier"
    symbol = '🛳 '

class Destroyer(Ship):
    _length = 1
    name = "Destroyer"
    symbol = '🚣'

class Submarine(Ship):
    _length = 2
    name = "Submarine"
    symbol = '🛥 '

class Battleship(Ship):
    _length = 3
    name = "Battleship"
    symbol = '🚢'

SHIP_TYPES = [AircraftCarrier, Battleship, Submarine, Destroyer]


class Player(object):
    name = ""
    opponent = None

    _board = None
    _ships = None

    def __init__(self, name):
        self.name = name

        self._board = []
        for row in range(10):
            self._board.append([False] * 10)

        self._ships = []

    def place_ship(self, ship, col, row, direction):
        ship.place(col, row, direction)

        for col, row in ship.coords:

            if self._board[col][row]:
                raise ValueError("Already a ship there")

            else:
                self._board[col][row] = ship

        self._ships.append(ship)

    def place_ships(self):
        # Prompt player to add their ships

        for ship in SHIP_TYPES:

            while True:

                try:
                    place = input("\nPlace your %s (col row H/V, eg '00H') >" % ship.name)
                    col = int(place[0])
                    row = int(place[1])
                    direction = place[2].upper()
                    self.place_ship(ship(), col, row, direction)
                    print()
                    self.show_board(show_hidden=True)
                    break
                except (IndexError, ValueError) as e:
                    print("\n(%s: try again)" % e)

        print("\nDone!\n")

    def show_board(self, show_hidden=False):
        print(" ", end=' ')
        for coli in range(10):
            print("%s " % coli, end=' ')
        print()

        for rowi in range(10):

            print(rowi, end=' ')

            for coli in range(10):
                ship = self._board[coli][rowi]

                if ship == "*":
                    print(sysinfo.HIT("🔥"), end=' ')

                elif ship == "#":
                    print(sysinfo.SUNK("☠ "), end=' ')

                elif ship == "_":
                    print(sysinfo.WATER("__"), end=' ')

                elif not ship or not show_hidden:
                    # Square is empty OR is ennemy ship and you cant see yet
                    print(sysinfo.WATER("🌊"), end=' ')

                else:
                    # Cell has a ship and you are allowed to see it
                    print("%s" % ship.symbol, end=' ')

            print("")

    def handle_shot(self, col, row):

        ship = self._board[col][row]

        if not ship:
            self._board[col][row] = "_"
            print("Miss")

        elif isinstance(ship, Ship):

            ship.hits += 1
            print(sysinfo.HIT("Hit!"))
            self._board[col][row] = "*"

            if ship.is_sunk():
                for col, row in ship.coords:
                    self._board[col][row] = "#"
                print(sysinfo.SUNK("You sunk my " + ship.name))

        else:
            raise ValueError("You've already played there")

    def is_dead(self):

        return all(ship.is_sunk() for ship in self._ships)


class Game(object):

    player1 = None
    player2 = None
    player = None # current player

    def __init__(self, player1_name, player2_name):
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)

        self.player1.opponent = self.player2
        self.player2.opponent = self.player1

    def pick_start_player(self):
        # randomly picks starting player
        self.player = random.choice([self.player1, self.player2])

    def setup_ships(self):
        # Prompt players to place ships

        for i in range(2):
            print("=" * 60)
            print("%s: Place your ships(%s, turn away!)" % (
                self.player.name, self.player.opponent.name))
            self.player.place_ships()
            input("\nPress Enter to switch players >")
            print("\n" * 80) # scrolling other players info off screen
            self.player = self.player.opponent

    def play(self):
        while True:
            # Loop until someone wins

            print()
            print("=" * 40)
            print("\n%s, let's attack %s\n" % (
                self.player.name, self.player.opponent.name))
            self.player.opponent.show_board()

            while True:
                # Loop until a valid move is made

                try:
                    move = input("\nMove (col row, e.g. '00') >")
                    col = int(move[0])
                    row = int(move[1])
                    print()
                    self.player.opponent.handle_shot(col,row)

                    break

                except (ValueError, IndexError) as e:
                    print("\n(%s: try again)" % e)

            print()
            self.player.opponent.show_board()

            if self.player.opponent.is_dead():
                break

            self.player = self.player.opponent

        print("\n *** YOU WIN! ***")

def play(player1_name, player2_name):
    game = Game(player1_name, player2_name)
    game.pick_start_player()

    print(sysinfo.HIT("\n\n***BATTLESHIP: %s vs %s ***" % (
        game.player.name, game.player.opponent.name)))

    game.setup_ships()

    game.play()

