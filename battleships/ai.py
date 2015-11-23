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
        if len(self.history) == 1:
            # Only one hit so far. Do clockwise continuation method.
            h_pos = self.history[-1]
            while True:
                offset = random.randint(0, 3)
                if offset == 0:
                    # Position 1 (left):
                    if self.is_valid_pos(h_pos[0] - 1, h_pos[1]):
                        # Check if shot is valid.
                        return h_pos[0] - 1, h_pos[1]
                elif offset == 1:
                    # Position 2 (top):
                    if self.is_valid_pos(h_pos[0], h_pos[1] - 1):
                        # Check if shot is valid.
                        return h_pos[0], h_pos[1] - 1
                elif offset == 2:
                    # Position 3 (right):
                    if self.is_valid_pos(h_pos[0] + 1, h_pos[1]):
                        # Check if shot is valid.
                        return h_pos[0] + 1, h_pos[1]
                else:
                    # Position 4 (bottom):
                    if self.is_valid_pos(h_pos[0], h_pos[1] + 1):
                        # Check if shot is valid.
                        return h_pos[0], h_pos[1] + 1
        elif len(self.history) > 1:
            # Continue in correct direction.
            h_pos_1 = self.history[-1]
            h_pos_2 = self.history[-1]
            direction = min_pos = max_pos = -1
            if h_pos_1[0] == h_pos_2[0]:
                # Both in same column.
                direction = 0
                max_pos = max(self.history, key=lambda item: item[1])[1]
                min_pos = min(self.history, key=lambda item: item[1])[1]
            elif h_pos_1[1] == h_pos_1[1]:
                # Both in same row.
                direction = 1
                max_pos = max(self.history, key=lambda item: item[0])[0]
                min_pos = min(self.history, key=lambda item: item[0])[0]
            else:
                print("Fatal error: 0x0005",
                      file=sys.stderr)
                exit()
            if max_pos - min_pos > len(self.history) - 1:
                # There is a "hole" between the hits. Fill it first.
                while True:
                    n_pos = random.randint(min_pos + 1, max_pos - 1)
                    if direction == 0:
                        if self.is_valid_pos(h_pos_1[0], n_pos):
                            return h_pos_1[0], n_pos
                    elif direction == 1:
                        if self.is_valid_pos(n_pos, h_pos_1[1]):
                            return n_pos, h_pos_1[1]
                    else:
                        print("Fatal error: 0x0006",
                              file=sys.stderr)
                        exit()
            else:
                # Continue by appending shots.
                while True:
                    n_dir = random.randint(0, 1)
                    if n_dir == 0:
                        n_pos = min_pos - 1
                    else:
                        n_pos = max_pos + 1
                    if direction == 0:
                        if self.is_valid_pos(h_pos_1[0], n_pos):
                            return h_pos_1[0], n_pos
                    elif direction == 1:
                        if self.is_valid_pos(n_pos, h_pos_1[1]):
                            return n_pos, h_pos_1[1]
                    else:
                        print("Fatal error: 0x0007",
                              file=sys.stderr)
                        exit()
        else:
            # No history, chose a random location.
            while True:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                # Check if those coordinates have been chosen before.
                if self.is_valid_pos(x, y):
                    return x, y

    # Check if a position has been hit before, and if it is valid.
    # Returns true if NOT hit before, AND valid.
    def is_valid_pos(self, x, y):
        if 0 <= x <= 9 and 0 <= y <= 9:
            if self.tracking_board.coord[x][y] == 0:
                return True
        return False

    # Let the AI take a turn.
    def take_turn(self, next_player):
        print("\nThe computer is taking a shot...\n")
        x, y = self.get_target(next_player)
        has_hit = False
        hit_ship = None
        for s in next_player.ships:
            if s.intercept(x, y):
                hit_ship = s
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
            hit_ship.add_damage()
            # Clear the history if the ship was sunk.
            # Otherwise, extend the history.
            if hit_ship.lives == 0:
                self.history = []
            else:
                self.history.append((x, y))
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
        self.history = []
