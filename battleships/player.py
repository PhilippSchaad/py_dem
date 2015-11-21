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


# Player-Class.
class Player:

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
                pos_in = input("Example: A 8 horizontal  >> ")
                argin = pos_in.split()
                if len(argin) == 3:
                    # Check first argument validity.
                    try:
                        x = board.col_lookup(argin[0])
                    except ValueError:
                        print("Please enter a valid column!")
                        continue

                    # Check second argument validity.
                    try:
                        y = int(argin[1])
                        if not 0 <= y <= 9:
                            raise ValueError
                    except ValueError:
                        print("Please enter a valid row!")
                        continue

                    # Check third argument validity.
                    if argin[2] == "horizontal":
                        o = 0
                    elif argin[2] == "vertical":
                        o = 1
                    else:
                        print("Please enter 'horizontal' or 'vertical' as an orientation!")
                        continue

                    # Check if the chosen placement is valid.
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
                            break
                        else:
                            print("This ship placement is invalid!")
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
                            break
                        else:
                            print("This ship placement is invalid!")
                    else:
                        print("Fatal error")
                        exit()
                else:
                    print("Please use the format '[Column] [Row] [Orientation]!")

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
                    print("Fatal error")
                    exit()
        print("\nPlacement completed.\n")

    # Object creation method.
    def __init__(self, num):
        self.player_id = num
        self.own_board = board.Board()
        self.ships = [
                ship.Ship(5, 'Aircraft Carrier', self),
                ship.Ship(4, 'Battleship', self),
                ship.Ship(3, 'Cruiser', self),
                ship.Ship(3, 'Submarine', self),
                ship.Ship(2, 'Destroyer', self)
                ]
        return

