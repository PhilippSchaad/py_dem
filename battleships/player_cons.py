# ------------------------------------------- #
# File: player_cons.py                        #
# Brief: Player console object file.          #
# Author: Philipp Schaad                      #
# Creation Date: 011215                       #
# ------------------------------------------- #

# ------------------------------------------- #
# Copyright:                                  #
# This software is released under the GNU     #
# General Public License (GNU GPL). See the   #
# LICENSE.txt file for more information.      #
# ------------------------------------------- #

import player_base
import board_base
import ship


# Player-Console-Class.
class PlayerCons(player_base.PlayerBase):

    # Set the players ships.
    def place_ships(self):
        print("================================================")
        print("=================== Player", self.player_id, "===================")
        print("================================================")

        print("\nShip placement:")

        for s in self.ships:
            x = y = o = -1
            while True:
                print("")
                print(" |A|B|C|D|E|F|G|H|I|J|")
                for i in range(10):
                    print(i, "|", sep="", end="")
                    for j in range(10):
                        placeholder = " "
                        if self.own_board.coord[j][i] == 1:
                            placeholder = "0"
                        print(placeholder, "|", sep="", end="")
                    print("")
                print("")

                print("Where do you want to place your ", s.name, "?", sep="")
                raw_in = input("Example: A 8 horizontal  >> ")
                arg_in = raw_in.split()
                if len(arg_in) == 3:
                    # Check first argument validity.
                    try:
                        x = board_base.col_lookup(arg_in[0])
                    except ValueError:
                        print("Please enter a valid column!")
                        continue

                    # Check second argument validity.
                    try:
                        y = int(arg_in[1])
                        if not 0 <= y <= 9:
                            raise ValueError
                    except ValueError:
                        print("Please enter a valid row!")
                        continue

                    # Check third argument validity.
                    if arg_in[2] == "horizontal":
                        o = 0
                    elif arg_in[2] == "vertical":
                        o = 1
                    else:
                        print("Please enter 'horizontal' or 'vertical' as an orientation!")
                        continue

                    # Check if the chosen placement is valid.
                    if self.check_placement(s, x, y, o):
                        break
                    else:
                        print("Invalid placement!")
                else:
                    print("Please use the format '[Column] [Row] [Orientation]'!")

            # Finally place the ship.
            s.place(x, y, o)
            # Mark the corresponding board tiles as occupied.
            for i in range(s.size):
                if o == 0:
                    # Ship horizontal.
                    self.own_board.coord[x + i][y] = 1
                elif o == 1:
                    # Ship vertical.
                    self.own_board.coord[x][y + i] = 1
                else:
                    print("Fatal error: 0x0001",
                          file=sys.stderr)
                    exit()

        print("\nPlacement completed.\n")

    # Ask the player where to fire his next shot.
    def get_target(self, next_player):
        x = y = -1
        while True:
            # Grab the input from the player and separate the words into an array.
            arg_in = input("Enter a target [Column] [Row] (Eg: D 7) >> ").split()
            if len(arg_in) == 2:
                # Check first argument validity.
                try:
                    x = board.col_lookup(arg_in[0])
                except ValueError:
                    print("Please enter a valid column!")
                    continue

                # Check second argument validity.
                try:
                    y = int(arg_in[1])
                    if not 0 <= y <= 9:
                        raise ValueError
                except ValueError:
                    print("Please enter a valid row!")
                    continue

                # Check if this position has been shot before.
                if self.tracking_board.coord[x][y] != 0:
                    print("You have shot this spot before!")
                else:
                    break
            else:
                print("Please use the format '[Column] [Row]'!")

        # Check if the shot results in a hit or not.
        for s in next_player.ships:
            if s.intercept(x, y):
                # We got a hit with ship s.
                print("Hit!")
                # Mark it on the tracking board.
                self.tracking_board.coord[x][y] = \
                    next_player.own_board.coord[x][y] = 2
                # Add damage to the ship.
                if s.add_damage():
                    # If the ship got sunk, mark it's perimeter.
                    self.mark_perimeter(s)
                return
        # If we fall through to here, we got a miss.
        print("Miss!")
        # Mark the miss on the tracking board.
        self.tracking_board.coord[x][y] = \
            next_player.own_board.coord[x][y] = 3

    # Override the base-class provided take_turn function.
    def take_turn(self, next_player):
        # Draw the board / situation to the screen.
        self.draw_board()
        self.get_target(next_player)
        input("Hit ENTER to continue...")

    # Draw the board-screen to the console.
    def draw_board(self):
        print("================================================")
        print("=================== Player", self.player_id, "===================")
        print("================================================")
        print("                       []")
        print("Your Board:            [] Tracking Board:")
        print("                       []")
        print(" |A|B|C|D|E|F|G|H|I|J| []  |A|B|C|D|E|F|G|H|I|J|")

        for i in range(10):
            print(i, "|", sep="", end="")
            for j in range(10):
                placeholder = " "
                if self.own_board.coord[j][i] == 1:
                    placeholder = "0"
                elif self.own_board.coord[j][i] == 2:
                    placeholder = "x"
                elif self.own_board.coord[j][i] == 3:
                    placeholder = "*"
                print(placeholder, "|", sep="", end="")
            print(" [] ", end="")

            print(i, "|", sep="", end="")
            for j in range(10):
                placeholder = " "
                if self.tracking_board.coord[j][i] == 2:
                    placeholder = "x"
                elif self.tracking_board.coord[j][i] == 3:
                    placeholder = "*"
                elif self.tracking_board.coord[j][i] == 4:
                    placeholder = "~"
                print(placeholder, "|", sep="", end="")
            print("")

        print("                       []")
        print("0 - Intact ship tile   [] x - Hit!")
        print("x - Damaged ship tile  [] * - Missed shot")
        print("* - Missed shot        [] ~ - Impossible Pos.")
        print("                       []")
        print("------------------------------------------------")

    # Object creation method.
    def __init__(self, num, ai=False):
        super().__init__(num, ai)
        self.own_board = board_base.Board()
        self.tracking_board = board_base.Board()
        # TODO: temporary.
        self.ships = [
                ship.Ship(5, 'Aircraft Carrier', self),
                ship.Ship(4, 'Battleship', self),
                ship.Ship(3, 'Cruiser', self),
                ship.Ship(3, 'Submarine', self),
                ship.Ship(2, 'Destroyer', self)
                ]

