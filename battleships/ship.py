# ------------------------------------------- #
# File: ship.py                               #
# Brief: Ship object file.                    #
# Author: Philipp Schaad                      #
# Creation Date: 191115                       #
# ------------------------------------------- #

# ------------------------------------------- #
# Copyright:                                  #
# This software is released under the GNU     #
# General Public License (GNU GPL). See the   #
# LICENSE.txt file for more information.      #
# ------------------------------------------- #


# Ship-Class.
class Ship:

    # Place the ship at a position and orientation.
    def place(self, p_x, p_y, p_or):
        self.x_pos = p_x
        self.y_pos = p_y
        self.orientation = p_or

    # Check if a given position intercepts with the ship.
    def intercept(self, x, y):
        if self.orientation == 0:
            # The ship is horizontal.
            if self.y_pos == y:
                if self.x_pos <= x < self.x_pos + self.size:
                    return True
        elif self.orientation == 1:
            # The ship is vertical.
            if self.x_pos == x:
                if self.y_pos <= y < self.y_pos + self.size:
                    return True
        # Fall-through: No interception.
        return False

    # Add one damage to the ship.
    def add_damage(self):
        self.lives -= 1
        if self.lives <= 0:
            print("Player", self.owner.player_id, "'s",
                  self.name, "has been sunk!")

    # Object creation method.
    def __init__(self, p_size, p_name, p_owner):
        self.size = p_size
        self.lives = self.size
        self.owner = p_owner
        self.name = p_name
        self.x_pos = self.y_pos = self.orientation = -1

