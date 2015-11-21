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

import player

import sys


# The Application itself.
class BattleshipsApplication:

    # Application start method.
    def start(self):
        self.players[0].place_ships()
        self.players[0].ships[0].place(4, 2, 0)
        if self.players[0].ships[0].intercept(6, 2):
            print("Hit!")
        else:
            print("Miss!")
        self.players[0].ships[0].add_damage()
        self.players[0].ships[0].add_damage()
        self.players[0].ships[0].add_damage()
        self.players[0].ships[0].add_damage()
        self.players[0].ships[0].add_damage()

    # Application setup method.
    def setup(self):
        self.n_players = get_players()
        if self.n_players == 1:
            # TODO
            return
        else:
            self.players = [
                    player.Player(1),
                    player.Player(2)
                    ]

    # Object creation method for the Battleships class.
    def __init__(self, gui=False):
        self.n_players = 0
        self.players = [None, None]

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
    app = None
    # Check the launch arguments to see whether the user
    # wants to start a GUI or not.
    if len(sys.argv) == 2 and sys.argv[1] == "--gui":
        print("Gui not implemented. Sorry!")
        exit()
        # TODO: Implement
        # app = BattleshipsApplication(gui=True)
    elif len(sys.argv) > 1:
        print("Invalid arguments")
        exit()
    else:
        app = BattleshipsApplication()

    if app is None:
        print("Fatal Error initializing the application")
        exit()
    
    # Initialize the application, according to the launch args.
    app.setup()
    app.start()

