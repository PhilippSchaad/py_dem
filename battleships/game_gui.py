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
black = pygame.Color(0, 0, 0, 255)
white = pygame.Color(255, 255, 255, 255)
red = pygame.Color(255, 0, 0, 255)
light_red = pygame.Color(255, 100, 100, 255)
green = pygame.Color(0, 255, 0, 255)
ligh_green = pygame.Color(100, 255, 100, 255)
blue = pygame.Color(0, 0, 255, 255)
light_blue = pygame.Color(100, 100, 255, 255)


# The GUI variant of the Application.
class GuiApplication:

    # Application start method.
    def start(self):
        return

    # Application setup method.
    def setup(self):
        self.window = pygame.display.set_mode((600, 300))
        pygame.display.set_caption("Battleships")
        self.get_players()

    # Display the player selection mode and get the player number.
    def get_players(self):
        # Show two buttons, one for 1 player, one for 2 players. Wait for action.
        sp_button = Button(self, 50, 50, 100, 50, "1 Player", red, light_red)
        mp_button = Button(self, 200, 50, 100, 50, "2 Players", blue, light_blue)
        print(sp_button.color, sp_button.a_color)

        while True:
            for event in pygame.event.get():
                pass
            mpos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            sp_button.show(mpos[0], mpos[1], click)
            mp_button.show(mpos[0], mpos[1], click)
            
            pygame.display.update()
            self.clock.tick(5)

    # Create a text object with a given color, font and message.
    def make_text(self, text, color, font):
        return self.std_font.render(text, True, color)

    # Object creation method.
    def __init__(self):
        self.n_players = self.turn = 0
        self.players = self.c_player = None
        self.running = False
        self.window = None
        pygame.init()
        self.clock = pygame.time.Clock()
        self.std_font = pygame.font.SysFont("LiberationMono-Regular", 25, False, False)
        # self.std_font = pygame.font.Font("font/bnmachine.ttf", 40)

        
# Button object class.
class Button:

    # Display the button.
    def show(self, posx, posy, click):
        if self.x + self.width > posx > self.x \
                and self.y + self.height > posy > self.y:
            self.parent.window.fill(self.a_color, rect=[self.x, self.y, self.width, self.height])
            if click and self.handler != None:
                self.handler()
        else:
            self.parent.window.fill(self.color, rect=[self.x, self.y, self.width, self.height])
        # Add the message.
        if self.msg != None:
            self.txt = self.parent.std_font.render(self.msg, True, black)
            rect = self.txt.get_rect()
            rect.center = (int(self.x + (self.width / 2)), int(self.y + (self.height / 2)))
            self.parent.window.blit(self.txt, rect)

    # Object creation method.
    def __init__(self, p_parent, p_x, p_y, p_width, p_height, p_msg=None, p_color=white, p_a_color=white, p_handler=None):
        self.x = p_x
        self.y = p_y
        self.width = p_width
        self.height = p_height
        self.msg = p_msg
        self.txt = None
        self.handler = p_handler
        self.parent = p_parent
        self.a_color = p_a_color
        self.color = p_color
        
