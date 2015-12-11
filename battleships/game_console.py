# ------------------------------------------- #
# File: game_console.py                       #
# Brief: Console version of the game.         #
# Author: Philipp Schaad                      #
# Creation Date: 231115                       #
# ------------------------------------------- #

# ------------------------------------------- #
# Copyright:                                  #
# This software is released under the GNU     #
# General Public License (GNU GPL). See the   #
# LICENSE.txt file for more information.      #
# ------------------------------------------- #

import player_cons
import ai_cons
import util


# The Console variant of the Application.
class ConsoleApplication:

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
            next_player = self.players[(self.turn + 1) % 2]
            self.c_player.take_turn(next_player)
            if next_player.check_vitals():
                self.next_player()
            else:
                self.running = False
                print("================================================")
                print("================== Game over! ==================")
                print("================================================")
                print("Player", self.c_player.player_id, "won the game!")

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
                util.clear_output()
            print("================================================")
            print("Switching players!")
            print("Player, ", self.c_player.player_id, ", are you ready?", sep="")
            input("Hit ENTER to continue...")
            print("================================================")
            if self.n_players == 2:
                util.clear_output()

    # Application setup method.
    def setup(self):
        self.n_players = get_players()
        if self.n_players == 1:
            self.players = [
                player_cons.PlayerCons(1),
                ai_cons.AICons(2)
            ]
        else:
            self.players = [
                player_cons.PlayerCons(1),
                player_cons.PlayerCons(2)
            ]

    # Object creation method for the Battleships class.
    def __init__(self):
        self.n_players = self.turn = 0
        self.players = self.c_player = None
        self.running = False


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
