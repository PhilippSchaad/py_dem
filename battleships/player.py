# ------------------------------------------- #
# File: player.py                             #
# Brief: Player object file.                  #
# Author: Philipp Schaad                      #
# Creation Date: 191115                       #
# ------------------------------------------- #

# ------------------------------------------- #
# Copyright:                                  #
# This software is released under the GNU     #
# General Public License (GNU GPL). See the   #
# LICENSE.txt file for more information.      #
# ------------------------------------------- #

import ship
import board

import sys


# Player-Class.
class Player(object):

    # Check if the player still is "alive" / has not lost yet.
    def check_vitals(self):
        for s in self.ships:
            if s.lives > 0:
                return True
        return False

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

    # Mark the boundaries of a ship after it has been sunk.
    def mark_perimeter(self, s):
        if s.orientation == 0:
            # Horizontal ship.
            for i in range(-1, 2):
                for j in range(-1, s.size + 1):
                    if 0 <= s.y_pos + i <= 9 and 0 <= s.x_pos + j <= 9:
                        if self.tracking_board.coord[s.x_pos + j][s.y_pos + i] == 0:
                            self.tracking_board.coord[s.x_pos + j][s.y_pos + i] = 4
        else:
            # Vertical ship.
            for i in range(-1, 2):
                for j in range(-1, s.size + 1):
                    if 0 <= s.y_pos + j <= 9 and 0 <= s.x_pos + i <= 9:
                        if self.tracking_board.coord[s.x_pos + i][s.y_pos + j] == 0:
                            self.tracking_board.coord[s.x_pos + i][s.y_pos + j] = 4

    # Take a turn.
    def take_turn(self, next_player):
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
        self.get_target(next_player)
        input("Hit ENTER to continue...")
        return

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

    # Check if a chosen ship placement is valid.
    def check_placement(self, s, x, y, o):
        if o == 0:
            # Ship horizontal.
            if x + s.size - 1 > 9:
                # Ship violates board-boundaries, invalid placement.
                return False
            else:
                # Check if it overlaps or touches a ship. Return false if yes.
                for i in range(-1, 2):
                    for j in range(-1, s.size + 1):
                        if 0 <= y + i <= 9 and 0 <= x + j <= 9:
                            if self.own_board.coord[x + j][y + i] == 1:
                                return False
        elif o == 1:
            # Ship vertical.
            if y + s.size - 1 > 9:
                # Ship violates board-boundaries, invalid placement.
                return False
            else:
                # Check if it overlaps or touches a ship. Return false if yes.
                for i in range(-1, 2):
                    for j in range(-1, s.size + 1):
                        if 0 <= y + j <= 9 and 0 <= x + i <= 9:
                            if self.own_board.coord[x + i][y + j] == 1:
                                return False
        else:
            print("Fatal error: 0x0003",
                  file=sys.stderr)
            exit()
        return True

    # Object creation method.
    def __init__(self, num, ai=False):
        self.is_ai = ai
        self.player_id = num
        self.own_board = board.Board()
        self.tracking_board = board.Board()
        self.ships = [
                ship.Ship(5, 'Aircraft Carrier', self),
                ship.Ship(4, 'Battleship', self),
                ship.Ship(3, 'Cruiser', self),
                ship.Ship(3, 'Submarine', self),
                ship.Ship(2, 'Destroyer', self)
                ]
        return
