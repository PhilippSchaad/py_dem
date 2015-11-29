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

import ai
import gui_player

import pygame


# Constants:
C_BLACK = pygame.Color('black')
C_WHITE = pygame.Color('white')
BG_COLOR = pygame.Color('#999999')


# The GUI variant of the Application.
class GuiApplication:

    # Application start method.
    def start(self):
        self.get_players()
        self.get_ship_placement()

        self.window = pygame.display.set_mode((755, 460))
        self.window.fill(BG_COLOR)
        self.running = True
        self.next_player()
        # Main Game-Loop:
        while self.running:
            next_player = self.players[self.turn % 2]
            self.c_player.take_turn(next_player)
            if next_player.check_vitals():
                self.next_player()
            else:
                self.running = False
                # TODO Game over screen.

    # Application setup method.
    def setup(self):
        self.clock = pygame.time.Clock()
        self.std_font = pygame.font.Font("font/ECAMa.ttf", 18)
        self.window = pygame.display.set_mode((350, 250))
        pygame.display.set_caption("Battleships")
        pygame.mouse.set_cursor(*pygame.cursors.diamond)

    # Switch to the next player. This also prevents the new player
    # from seeing any information about the previous one and vice
    # versa, in case 2 human players are playing.
    def next_player(self):
        self.c_player = self.players[self.turn % 2]
        self.window.fill(BG_COLOR)
        if self.c_player.is_ai:
            Button(self, 202, 200, 350, 40,
                   "The Computer is taking his turn",
                   pygame.Color('#00ff00'), pygame.Color('#00ff00')).show(0, 0, (0, 0, 0))
            pygame.display.update()
        else:
            # Check if the player is ready to play.
            ready_button = Button(self, 247, 205, 260, 50,
                                  "Player " + str(self.c_player.player_id) + " ready to play",
                                  pygame.Color('#00ff00'), pygame.Color('#99ff99'),
                                  self.ready_to_play)
            while not self.player_ready:
                click = (0, 0, 0)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.close_app()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        click = (1, 0, 0)
                    else:
                        pass
                mouse_pos = pygame.mouse.get_pos()

                ready_button.show(mouse_pos[0], mouse_pos[1], click)

                pygame.display.update()
                self.clock.tick(15)
        self.turn += 1

    # Display a single grid to let the player place his ships.
    def get_ship_placement(self):
        for p in self.players:
            if not p.is_ai:
                self.window = pygame.display.set_mode((570, 460))
                self.window.fill(BG_COLOR)

                # Check if the player is ready to place.
                ready_button = Button(self, 155, 205, 260, 50,
                                      "Player " + str(p.player_id) + " ready to place",
                                      pygame.Color('#00ff00'), pygame.Color('#99ff99'),
                                      self.ready_to_play)
                while not self.player_ready:
                    click = (0, 0, 0)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.close_app()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            click = (1, 0, 0)
                        else:
                            pass
                    mouse_pos = pygame.mouse.get_pos()

                    ready_button.show(mouse_pos[0], mouse_pos[1], click)

                    pygame.display.update()
                    self.clock.tick(15)

                # Do the placement.
                p.place_ships()

                self.player_ready = False
            else:
                self.window.fill(BG_COLOR)
                Button(self, 100, 200, 350, 40,
                       "The Computer is placing his ships",
                       pygame.Color('#00ff00'), pygame.Color('#00ff00')).show(0, 0, (0, 0, 0))
                pygame.display.update()
                # Let the AI place its ships.
                p.place_ships()

    # Display the player selection mode and get the player number.
    def get_players(self):
        self.window.fill(BG_COLOR)
        # Show two buttons, one for 1 player, one for 2 players. Wait for action.
        sp_button = Button(self, 50, 50, 100, 50, "1 Player",
                           pygame.Color('#00ff00'), pygame.Color('#99ff99'),
                           self.set_one_player)
        mp_button = Button(self, 200, 50, 100, 50, "2 Players",
                           pygame.Color('#0000ff'), pygame.Color('#9999ff'),
                           self.set_two_players)
        quit_button = Button(self, 125, 150, 100, 50, "Quit",
                             pygame.Color('#ff0000'), pygame.Color('#ff9999'),
                             self.close_app)

        while self.n_players == 0:
            click = (0, 0, 0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close_app()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = (1, 0, 0)
                else:
                    pass
            mouse_pos = pygame.mouse.get_pos()

            sp_button.show(mouse_pos[0], mouse_pos[1], click)
            mp_button.show(mouse_pos[0], mouse_pos[1], click)
            quit_button.show(mouse_pos[0], mouse_pos[1], click)
            
            pygame.display.update()
            self.clock.tick(15)

        if self.n_players == 1:
            self.players = [
                gui_player.GuiPlayer(self, 1),
                ai.AI(2, console=False)
            ]
        else:
            self.players = [
                gui_player.GuiPlayer(self, 1),
                gui_player.GuiPlayer(self, 2)
            ]

    # Set the number of players to be one.
    def set_one_player(self):
        self.n_players = 1

    # Set the number of players to be one.
    def set_two_players(self):
        self.n_players = 2

    def ready_to_play(self):
        self.player_ready = not self.player_ready

    # Close the application correctly
    @staticmethod
    def close_app():
        pygame.display.quit()
        pygame.quit()
        quit()

    # Object creation method.
    def __init__(self):
        pygame.init()
        self.n_players = self.turn = 0
        self.players = []
        self.c_player = None
        self.window = self.std_font = self.clock = None
        self.running = self.player_ready = False


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
            self.txt = self.parent.std_font.render(self.msg, True, C_BLACK)
            rect = self.txt.get_rect()
            rect.center = (int(self.x + (self.width / 2)), int(self.y + (self.height / 2)))
            self.parent.window.blit(self.txt, rect)

    # Object creation method.
    def __init__(self, p_parent, p_x, p_y, p_width, p_height,
                 p_msg=None, p_color=C_WHITE, p_a_color=C_WHITE, p_handler=None):
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
