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

import sys


# The Application itself.
class BattleshipsApplication:

    # Application setup method.
    def setup(self):
        print(self.has_gui)

    # Object creation method for the Battleships class.
    def __init__(self, gui=False):
        if gui:
            self.has_gui = "We have gui!"
        else:
            self.has_gui = "We do NOT have gui!"


# ========================================== #

# Application entry point.
if __name__ == "__main__":
    # Check the launch arguments to see whether the user
    # wants to start a GUI or not.
    if len(sys.argv) == 2 and sys.argv[1] == "--gui":
        app = BattleshipsApplication(gui=True)
    elif len(sys.argv) > 1:
        print("Invalid arguments")
        exit()
    else:
        app = BattleshipsApplication()
    
    # Initialize the application, according to the launch args.
    app.setup()
