# ------------------------------------------- #
# File: gui_player.py                         #
# Brief: Player object file for the GUI.      #
# Author: Philipp Schaad                      #
# Creation Date: 271115                       #
# ------------------------------------------- #

# ------------------------------------------- #
# Copyright:                                  #
# This software is released under the GNU     #
# General Public License (GNU GPL). See the   #
# LICENSE.txt file for more information.      #
# ------------------------------------------- #

import gui_board
import player

import pygame


# Object class.
class GuiPlayer(player.Player):

    # Override the get-target function.
    def get_target(self, next_player):
        return

    # Override the take-turn function.
    def take_turn(self, next_player):
        return

    # Override the ship placement method.
    def place_ships(self):
        for s in self.ships:
            x = y = -1
            o = 0  # Orientation.
            is_valid = False
            # Keeps track of the current loop (Checks if we are done placing one ship.)
            placing_ship = True
            while placing_ship:
                self.parent.window.fill(pygame.Color('#999999'))
                self.parent.window.fill(pygame.Color('#000000'), rect=[190, 0, 5, 460])
                self.own_board.draw(215, 20)

                mouse_pos = pygame.mouse.get_pos()
                board_pos = gui_board.get_coord(215, 20, mouse_pos[0], mouse_pos[1])
                if board_pos is not None:
                    x = board_pos[0]
                    y = board_pos[1]
                    highlight_color = pygame.Color('#ff0000')
                    is_valid = self.check_placement(s, x, y, o)
                    if is_valid:
                        highlight_color = pygame.Color('#ffff00')
                    if o == 0:
                        # Ship horizontal.
                        self.own_board.highlight(215, 20, x, y,
                                                 s.size, 1, highlight_color)
                    else:
                        # Ship vertical.
                        self.own_board.highlight(215, 20, x, y,
                                                 1, s.size, highlight_color)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.parent.close_app()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            if o == 0:
                                o = 1
                            else:
                                o = 0
                        else:
                            pass
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if is_valid:
                            # Place the ship.
                            s.place(x, y, o)
                            # Mark the board accordingly.
                            for i in range(s.size):
                                if o == 0:
                                    self.own_board.coord[x + i][y] = 1
                                else:
                                    self.own_board.coord[x][y + i] = 1
                            placing_ship = False
                    else:
                        pass

                pygame.display.update()
                self.parent.clock.tick(15)

    # Object creation method.
    def __init__(self, p_parent, num, ai=False):
        super(GuiPlayer, self).__init__(num, ai)
        self.own_board = gui_board.GuiBoard(p_parent)
        self.tracking_board = gui_board.GuiBoard(p_parent)
        self.parent = p_parent
