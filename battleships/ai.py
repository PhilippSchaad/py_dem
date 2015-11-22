# ------------------------------------------- #
# File: ai.py                                 #
# Brief: AI-Module of the battleships-app.    #
# Author: Philipp Schaad                      #
# Creation Date: 201115                       #
# ------------------------------------------- #

# ------------------------------------------- #
# Copyright:                                  #
# This software is released under the GNU     #
# General Public License (GNU GPL). See the   #
# LICENSE.txt file for more information.      #
# ------------------------------------------- #

import player
import board

import random
import sys
from time import sleep


# Artificial intelligence class.
class AI(player.Player):

    # Let the AI take a shot.
    def get_target(self, next_player):
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            # Check if those coordinates have been chosen before.
            if self.tracking_board.coord[x][y] == 0:
                return x, y

    # Let the AI take a turn.
    def take_turn(self, next_player):
        print("\nThe computer is taking a shot...\n")
        x, y = self.get_target(next_player)
        has_hit = False
        for s in next_player.ships:
            if s.intercept(x, y):
                s.add_damage()
                has_hit = True
                break
        col = None
        for i, j in board.cols.items():
            if x == j:
                col = i
                break
        sleep(1)
        print("\nThe computer shoots at", col, y)
        if has_hit:
            print("This is a hit!")
            self.tracking_board.coord[x][y] = \
                next_player.own_board.coord[x][y] = 2
        else:
            print("This is a miss...")
            self.tracking_board.coord[x][y] = \
                next_player.own_board.coord[x][y] = 3
        print("\nThe computer's turn is over.\n")
        sleep(1)

    # Let the AI place it's ships.
    def place_ships(self):
        print("\nThe computer is placing ships...\n")
        for s in self.ships:
            while True:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                o = random.randint(0, 1)

                # Check if the chosen placement is valid.
                if self.check_placement(s, x, y, o):
                    break

            # Place the ship
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
                    print("Fatal error: 0x0002",
                          file=sys.stderr)
                    exit()
        sleep(1)
        print("\nThe computer finished placing his ships.\n")
        sleep(1)

    # Object creation method.
    def __init__(self, p_num):
        super(AI, self).__init__(p_num, True)
        random.seed()
