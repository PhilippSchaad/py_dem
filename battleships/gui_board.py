# ------------------------------------------- #
# File: gui_board.py                          #
# Brief: Board object file for the GUI.       #
# Author: Philipp Schaad                      #
# Creation Date: 271115                       #
# ------------------------------------------- #

# ------------------------------------------- #
# Copyright:                                  #
# This software is released under the GNU     #
# General Public License (GNU GPL). See the   #
# LICENSE.txt file for more information.      #
# ------------------------------------------- #

import board

import pygame


# Object class.
class GuiBoard(board.Board):

    # Highlight a/some tiles.
    def highlight(self, b_x, b_y, col, row, width, height, color):
        for i in range(width):
            for j in range(height):
                if 0 <= col + i <= 9 and 0 <= row + j <= 9:
                    self.parent.window.fill(color,
                                            rect=[b_x + 35 + (col * 30) + (i * 30),
                                                  b_y + 35 + (row * 30) + (j * 30), 25, 2])
                    self.parent.window.fill(color,
                                            rect=[b_x + 35 + (col * 30) + (i * 30),
                                                  b_y + 58 + (row * 30) + (j * 30), 25, 2])
                    self.parent.window.fill(color,
                                            rect=[b_x + 35 + (col * 30) + (i * 30),
                                                  b_y + 35 + (row * 30) + (j * 30), 2, 25])
                    self.parent.window.fill(color,
                                            rect=[b_x + 58 + (col * 30) + (i * 30),
                                                  b_y + 35 + (row * 30) + (j * 30), 2, 25])

    # Draw the board to the screen, at a given position.
    def draw(self, x, y):
        for i in range(11):
            self.parent.window.fill(pygame.Color('#000000'),
                                    rect=[x + ((i + 1) * 30), y + 5, 5, 330])
            self.parent.window.fill(pygame.Color('#000000'),
                                    rect=[x + 5, y + ((i + 1) * 30), 330, 5])
        col_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        row_names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for i in range(10):
            char = self.parent.std_font.render(col_names[i], True,
                                               pygame.Color('#000000'))
            char_rect = char.get_rect()
            char_rect.center = (x + 47 + (i * 30), y + 17)
            self.parent.window.blit(char, char_rect)
            num = self.parent.std_font.render(row_names[i], True,
                                              pygame.Color('#000000'))
            num_rect = num.get_rect()
            num_rect.center = (x + 17, y + 47 + (i * 30))
            self.parent.window.blit(num, num_rect)
        for i in range(10):
            for j in range(10):
                if self.coord[j][i] == 1:
                    self.parent.window.fill(pygame.Color('#00ff00'),
                                            rect=[x + 35 + (j * 30), y + 35 + (i * 30), 25, 25])
                elif self.coord[j][i] == 2:
                    self.parent.window.fill(pygame.Color('#00ff00'),
                                            rect=[x + 35 + (j * 30), y + 35 + (i * 30), 25, 25])
                    pygame.draw.line(self.parent.window, pygame.Color('#ff0000'),
                                     (x + 37 + (j * 30), y + 35 + (i * 30)),
                                     (x + 58 + (j * 30), y + 60 + (i * 30)), 5)
                    pygame.draw.line(self.parent.window, pygame.Color('#ff0000'),
                                     (x + 37 + (j * 30), y + 60 + (i * 30)),
                                     (x + 58 + (j * 30), y + 35 + (i * 30)), 5)
                elif self.coord[j][i] == 3:
                    pygame.draw.circle(self.parent.window, pygame.Color('#0000ff'),
                                       (x + 47 + (j * 30), y + 47 + (i * 30)), 10, 5)

    # Object creation method.
    def __init__(self, p_parent):
        super(GuiBoard, self).__init__()
        self.parent = p_parent


# Figure out the row/column of the mouse relative to a board.
def get_coord(b_x, b_y, x, y):
    if x < b_x + 35 or x > b_x + 325 or y < b_y + 35 or y > b_y + 325:
        return None
    else:
        col = row = -1
        base_x = b_x + 35
        base_y = b_y + 35
        for i in range(10):
            if base_x < x < base_x + 25:
                col = i
            if base_y < y < base_y + 25:
                row = i
            base_x += 30
            base_y += 30
        if col == -1 or row == -1:
            return None
        else:
            return col, row
