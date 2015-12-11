# ------------------------------------------- #
# File: ai_cons.py                            #
# Brief: Console extension for the AI.        #
# Author: Philipp Schaad                      #
# Creation Date: 081215                       #
# ------------------------------------------- #

# ------------------------------------------- #
# Copyright:                                  #
# This software is released under the GNU     #
# General Public License (GNU GPL). See the   #
# LICENSE.txt file for more information.      #
# ------------------------------------------- #

import ai_base
import board

from time import sleep


# AI Console extension
class AICons(ai_base.AI):

    def take_turn(self, next_player):
        print("\nThe computer is taking a shot...\n")
        x, y = self.get_target()
        sleep(1)
        # Print out the chosen target. (Looks it up in the columns lookup table)
        for i, j in board.cols.items():
            if x == j:
                print("\nThe computer shoots at", i, y)
                break

        # Check if the shot results in a hit or not.
        for s in next_player.ships:
            if s.intercept(x, y):
                # We got a hit with ship s.
                print("This is a hit!")
                # Mark it on the tracking board.
                self.tracking_board.coord[x][y] = \
                    next_player.own_board.coord[x][y] = 2
                # Add damage to the ship.
                if s.add_damage():
                    # If the ship got sunk:
                    # Clear the history and mark the perimeter.
                    self.history = []
                    self.mark_perimeter(s)
                else:
                    # Otherwise, extend the history.
                    self.history.append((x, y))
                sleep(1)
                return
        # If we fall through to here, we got a miss.
        print("This is a miss...")
        self.tracking_board.coord[x][y] = \
            next_player.own_board.coord[x][y] = 3
        sleep(1)

    def place_ships(self):
        print("\nThe computer is placing his ships...\n")
        super(AICons, self).place_ships()
        print("\nThe computer finished placing his ships.\n")
        sleep(1)
