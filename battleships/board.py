# ------------------------------------------- #
# File: board.py                              #
# Brief: Board object file.                   #
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


# Board-Class.
class Board:

    # Set up the board.
    def setup(self):
        return

    # Add a ship to the board, at a given position.

    # Object cretaion method.
    def __init__(self):
        self.width = self.height = 10
        self.n_fields = self.width * self.height

        # Initialize the Coordinate-System.
        self.coord = \
            [[0 for _ in range(self.height)] for _ in range(self.width)]
