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
black = pygame.Color('black')
white = pygame.Color('white')


# The GUI variant of the Application.
class GuiApplication:

    # Application start method.
    def start(self):
        self.get_players()
        self.get_ship_placement()

    # Application setup method.
    def setup(self):
        self.window = pygame.display.set_mode((350, 250))
        pygame.display.set_caption("Battleships")
        pygame.mouse.set_cursor(*pygame.cursors.diamond)

    # Display a single grid to let the player place his ships.
    def get_ship_placement(self):
        self.window = pygame.display.set_mode((460, 460))

    # Display the player selection mode and get the player number.
    def get_players(self):
        # Show two buttons, one for 1 player, one for 2 players. Wait for action.
        sp_button = Button(self, 50, 50, 100, 50, "1 Player",
                           pygame.Color('#00ff00'), pygame.Color('#99ff99'))
        mp_button = Button(self, 200, 50, 100, 50, "2 Players",
                           pygame.Color('#0000ff'), pygame.Color('#9999ff'))
        quit_button = Button(self, 125, 150, 100, 50, "Quit",
                             pygame.Color('#ff0000'), pygame.Color('#ff9999'), close_app)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close_app()
                else:
                    pass
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            sp_button.show(mouse_pos[0], mouse_pos[1], click)
            mp_button.show(mouse_pos[0], mouse_pos[1], click)
            quit_button.show(mouse_pos[0], mouse_pos[1], click)
            
            pygame.display.update()
            self.clock.tick(15)

    # Object creation method.
    def __init__(self):
        self.n_players = self.turn = 0
        self.players = self.c_player = None
        self.running = False
        self.window = None
        pygame.init()
        self.clock = pygame.time.Clock()
        self.std_font = pygame.font.Font("font/ECAMa.ttf", 18)


# Close the application correctly
def close_app():
        pygame.display.quit()
        pygame.quit()
        quit()

        
# Button object class.
class Button:

    # Display the button.
    def show(self, pos_x, pos_y, click):
        if self.x + self.width > pos_x > self.x \
                and self.y + self.height > pos_y > self.y:
            self.parent.window.fill(self.a_color, rect=[self.x, self.y, self.width, self.height])
            if 1 in click and (self.handler is not None):
                self.handler()
        else:
            self.parent.window.fill(self.color, rect=[self.x, self.y, self.width, self.height])
        # Add the message.
        if self.msg is not None:
            self.txt = self.parent.std_font.render(self.msg, True, black)
            rect = self.txt.get_rect()
            rect.center = (int(self.x + (self.width / 2)), int(self.y + (self.height / 2)))
            self.parent.window.blit(self.txt, rect)

    # Object creation method.
    def __init__(self, p_parent, p_x, p_y, p_width, p_height,
                 p_msg=None, p_color=white, p_a_color=white, p_handler=None):
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
