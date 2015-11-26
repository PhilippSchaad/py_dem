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

import game_console
import game_gui

import sys


# Application entry point.
if __name__ == "__main__":
    app = None
    # Check the launch arguments to see whether the user
    # wants to start a GUI or not.
    if len(sys.argv) == 2 and sys.argv[1] == "--gui":
        # print("Gui not implemented. Sorry!")
        # exit()
        # TODO: Implement!
        app = game_gui.GuiApplication()
    elif len(sys.argv) > 1:
        print("Invalid arguments")
        exit()
    else:
        app = game_console.ConsoleApplication()

    if app is None:
        print("Fatal Error initializing the application",
              file=sys.stderr)
        exit()
    
    # Initialize the application, according to the launch args.
    app.setup()
    app.start()
