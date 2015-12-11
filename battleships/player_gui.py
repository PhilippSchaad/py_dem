# ------------------------------------------- #
# File: player_gui.py                         #
# Brief: Player object file for the GUI.      #
# Author: Philipp Schaad                      #
# Creation Date: 021215                       #
# ------------------------------------------- #

# ------------------------------------------- #
# Copyright:                                  #
# This software is released under the GNU     #
# General Public License (GNU GPL). See the   #
# LICENSE.txt file for more information.      #
# ------------------------------------------- #

import player_base
import board_gui
import ship_gui

import pygame


# Object class.
class PlayerGui(player_base.PlayerBase):

    # Override the get-target function.
    def get_target(self, next_player):
        x = y = -1
        while True:
            self.parent.window.fill(pygame.Color('#999999'))
            self.parent.window.fill(pygame.Color('#000000'), rect=[375, 0, 5, 460])
            self.own_board.draw(21, 21)
            self.tracking_board.draw(396, 21)

            mouse_pos = pygame.mouse.get_pos()
            board_pos = board_gui.get_coord(396, 21, mouse_pos[0], mouse_pos[1])
            if board_pos is not None:
                x = board_pos[0]
                y = board_pos[1]
                highlight_color = pygame.Color('#ff0000')
                if self.tracking_board.coord[x][y] == 0:
                    highlight_color = pygame.Color('#ffff00')
                self.tracking_board.highlight(396, 21, x, y, 1, 1, highlight_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.parent.close_app()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.tracking_board.coord[x][y] == 0:
                        for s in next_player.ships:
                            if s.intercept(x, y):
                                self.tracking_board.coord[x][y] = \
                                    next_player.own_board.coord[x][y] = 2
                                if s.add_damage():
                                    self.mark_perimeter(s)
                                return
                        # If we fall through to here, we got a miss.
                        self.tracking_board.coord[x][y] = \
                            next_player.own_board.coord[x][y] = 3
                        return
                else:
                    pass

            pygame.display.update()
            self.parent.clock.tick(15)

    # Override the take-turn function.
    def take_turn(self, next_player):
        self.get_target(next_player)
        self.parent.window.fill(pygame.Color('#999999'))
        self.parent.window.fill(pygame.Color('#000000'), rect=[375, 0, 5, 460])
        self.own_board.draw(21, 21)
        self.tracking_board.draw(396, 21)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.parent.close_app()
            else:
                pass
        pygame.display.update()
        pygame.time.wait(1000)

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
                board_pos = board_gui.get_coord(215, 20, mouse_pos[0], mouse_pos[1])
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
    def __init__(self, parent, num, ai=False):
        self.parent = parent
        super().__init__(num, ai)
        self.own_board = board_gui.BoardGUI(self.parent)
        self.tracking_board = board_gui.BoardGUI(self.parent)
        self.ships = [
                ship_gui.ShipGUI(5, 'Aircraft Carrier', self),
                ship_gui.ShipGUI(4, 'Battleship', self),
                ship_gui.ShipGUI(3, 'Cruiser', self),
                ship_gui.ShipGUI(3, 'Submarine', self),
                ship_gui.ShipGUI(2, 'Destroyer', self)
                ]
