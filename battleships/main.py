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
        self.running = True
        # Assign the first player
        self.c_player = self.players[self.turn % 2]

        # Let both players place their ships
        self.c_player.place_ships()
        self.next_player()
        self.c_player.place_ships()
        self.next_player()

        print("================================================")
        print("================ Game starting! ================")
        print("================================================")
        print("")

        # Main game loop.
        while self.running:
            self.c_player.take_turn()
            if self.players[(self.turn + 1) % 2].check_vitals():
                self.next_player()
            else:
                self.running = False
                print("================================================")
                print("================== Game over! ==================")
                print("================================================")
                print("Player", self.c_player.player_id, "won the game!")

        # if self.players[0].ships[0].intercept(6, 2):
        #     print("Hit!")
        # else:
        #     print("Miss!")
        # self.players[0].ships[0].add_damage()

    # Switch to the next player. This also prevents the new player
    # from seeing any information about the previous one and vice
    # versa, in case 2 human players are playing.
    def next_player(self):
        self.turn += 1
        self.c_player = self.players[self.turn % 2]
        if self.c_player.is_ai:
            print("================================================")
            print("Computer is playing!")
            print("================================================")
        else:
            if self.n_players == 2:
                clear_output()
            print("================================================")
            print("Switching players!")
            print("Player, ", self.c_player.player_id, ", are you ready?", sep="")
            input("Hit enter to confirm")
            print("================================================")
            if self.n_players == 2:
                clear_output()

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
        self.players = None
        self.turn = 0
        self.c_player = None
        self.running = False

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


# Clear the console output py printing 500 new lines.
def clear_output():
    for _ in range(500):
        print("")

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
