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
import util

import sys


# Player-Class.
class Player(object):

    # Check if the player still is "alive" / has not lost yet.
    def check_vitals(self):
        has_floating_ship = False
        for s in self.ships:
            if s.lives > 0:
                has_floating_ship = True
                break
        return has_floating_ship

    # Ask the player where to fire his next shot.
    def get_target(self, next_player):
        x = y = -1
        while True:
            raw_in = input("Enter a target [Column] [Row] (Eg: D 7) >> ")
            arg_in = raw_in.split()
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
        has_hit = False
        for s in next_player.ships:
            if s.intercept(x, y):
                s.add_damage()
                has_hit = True
                break
        if has_hit:
            print("Hit!")
            self.tracking_board.coord[x][y] = \
                next_player.own_board.coord[x][y] = 2
        else:
            print("Miss!")
            self.tracking_board.coord[x][y] = \
                next_player.own_board.coord[x][y] = 3

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
                print(placeholder, "|", sep="", end="")
            print("")

        print("                       []")
        print("0 - Intact ship tile   [] x - Hit!")
        print("x - Damaged ship tile  [] * - Missed shot")
        print("* - Missed shot        []")
        print("                       []")
        print("------------------------------------------------")
        self.get_target(next_player)
        input("Hit ENTER to continue...")
        util.pause(3)
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
            holds = True
            if x + s.size - 1 > 9:
                holds = False
            else:
                for i in range(s.size):
                    if self.own_board.coord[x + i][y] == 1:
                        holds = False
            if holds:
                return True
            else:
                return False
        elif o == 1:
            # Ship vertical.
            holds = True
            if y + s.size - 1 > 9:
                holds = False
            else:
                for i in range(s.size):
                    if self.own_board.coord[x][y + i] == 1:
                        holds = False
            if holds:
                return True
            else:
                return False
        else:
            print("Fatal error: 0x0003",
                  file=sys.stderr)
            exit()

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
