# ------------------------------------------- #
# File: game_gui.py                           #
# Brief: GUI version of the game.             #
# Author: Philipp Schaad                      #
# Creation Date: 231115                       #
# ------------------------------------------- #

# ------------------------------------------- #
# Copyright:                                  #
# This software is released under the GNU     #
# General Public License (GNU GPL). See the   #
# LICENSE.txt file for more information.      #
# ------------------------------------------- #

import pygame


# Constants:
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


# The GUI variant of the Application.
class GuiApplication:

    # Application start method.
    def start(self):
        return

    # Application setup method.
    def setup(self):
        self.window = pygame.display.set_mode((600, 300))
        pygame.display.set_caption("Battleships")

    # Display a button with a given text and action handler at a given position.
    def new_button(self, x, y, d_x, d_y, msg, color, handler):
        #     game_display.fill((255, 0, 0), rect=[box_x, box_y, 10, 10])
        self.window.fill(color, rect=[x, y, d_x, d_y])

    # Display the player selection mode and get the player number.
    def get_players(self):
        return

    # Object creation method.
    def __init__(self):
        self.n_players = self.turn = 0
        self.players = self.c_player = None
        self.running = False
        self.window = None
        pygame.init()
        self.std_font = pygame.font.Font("font/bnmachine.ttf", 40)
