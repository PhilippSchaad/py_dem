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


# Column lookup table.
cols = {
    "A": 0, "B": 1, "C": 2, "D": 3, "E": 4,
    "F": 5, "G": 6, "H": 7, "I": 8, "J": 9
}


# Board-Class.
class Board:

    # Object creation method.
    def __init__(self):
        self.width = self.height = 10

        # Initialize the Coordinate-System.
        self.coord = \
            [[0 for _ in range(self.height)] for _ in range(self.width)]


# Utility method to convert alpha-columns into numerical values.
def col_lookup(col):
    if col in cols:
        return cols[col]
    else:
        raise ValueError
