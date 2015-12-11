# ------------------------------------------- #
# File: player_base.py                        #
# Brief: Player base object file.             #
# Author: Philipp Schaad                      #
# Creation Date: 301115                       #
# ------------------------------------------- #

# ------------------------------------------- #
# Copyright:                                  #
# This software is released under the GNU     #
# General Public License (GNU GPL). See the   #
# LICENSE.txt file for more information.      #
# ------------------------------------------- #


# Player-Base-Class.
class PlayerBase(object):

    # Let the player take his turn.
    def take_turn(self, next_player):
        pass

    # Let the player place his ships.
    def place_ships(self):
        pass

    # Check if the player still is "alive" / has not lost yet.
    def check_vitals(self):
        for s in self.ships:
            if s.lives > 0:
                return True
        return False

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

    # Check if the desired placement of a ship is valid.
    def check_placement(self, s, x, y, o):
        # Check orientation of the ship.
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
        else:
            # Ship vertical. (o == 1)
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
        # If we fall through to here, the placement is valid.
        return True

    # Object creation procedure.
    def __init__(self, num, ai=False):
        self.is_ai = ai
        self.player_id = num
        self.own_board = self.tracking_board = None
        self.ships = []
