# ------------------------------------------- #
# File: main.py                               #
# Brief: Main entry point file for a simple / #
# / battle-ships game.                        #
# Author: Philipp Schaad                      #
# Creation Date: 191115                       #
# ------------------------------------------- #

# ------------------------------------------- #
# Copyright:                                  #
# This software is released under the GNU     #
# General Public License (GNU GPL). See the   #
# LICENSE.txt file for more information.      #
# ------------------------------------------- #

import board
import ai

import sys


# The Application itself.
class BattleshipsApplication:

    # Application setup method.
    def setup(self):
        self.n_players = get_players()

    # Object creation method for the Battleships class.
    def __init__(self, gui=False):
        return

# ========================================== #

# Ask the user for the number of players.
def get_players():
    while True:
        try:
            n_in = int(input("Number of players (1/2): "))
            if n_in == 1 or n_in == 2:
                return n_in
            else:
                raise ValueError
        except ValueError:
            print("Please enter a valid numerical value.")

# ========================================== #

# Application entry point.
if __name__ == "__main__":
    # Check the launch arguments to see whether the user
    # wants to start a GUI or not.
    if len(sys.argv) == 2 and sys.argv[1] == "--gui":
        print("Gui not implemented yet. Sorry!")
        exit()
        #app = BattleshipsApplication(gui=True)
    elif len(sys.argv) > 1:
        print("Invalid arguments")
        exit()
    else:
        app = BattleshipsApplication()
    
    # Initialize the application, according to the launch args.
    app.setup()
