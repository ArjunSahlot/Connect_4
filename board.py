#
#  Connect 4
#  A simple online connect-4 game in pygame.
#  Copyright Arjun Sahlot 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import pygame
from constants import ROWS, COLS, RADIUS, RED, YELLOW, BLACK, WHITE, WIDTH, HEIGHT
pygame.init()

FONT = pygame.font.SysFont("comicsans", 50)


class Board:
    def __init__(self):
        self.ready = False
        self._create_board()
        self.turn = "r"
        self.ready_players = 0

    def draw(self, win, anim_time):
        if self.ready:
            for col in range(len(self.board)):
                for row in range(len(self.board[col])):
                    if self.board[col][row] == "":
                        pygame.draw.circle(win, BLACK, (9 * (col + 1) + RADIUS + RADIUS * 2 * col, RADIUS * 3 + 9 * (row + 1) + RADIUS * 2 * row + 5), RADIUS)
                    else:
                        pygame.draw.circle(win, YELLOW if self.board[col][row] == "y" else RED, (9 * (col + 1) + RADIUS + RADIUS * 2 * col, RADIUS * 3 + 9 * (row + 1) + RADIUS * 2 * row + 5), RADIUS)
        else:
            win.fill(BLACK)
            multiplier = (anim_time//200)%4
            text = "Waiting for opponent" + "." * multiplier
            display_text = FONT.render(text, 1, WHITE)
            win.blit(display_text, (WIDTH//2 - display_text.get_width()//2, HEIGHT//2 - display_text.get_height()//2))

    def insert(self, col):
        if self.ready and not self.col_full(col):
            for pos in range(ROWS - 1, -1, -1):
                if self.board[col][pos] == "":
                    self.board[col][pos] = self.turn
                    break
            self.turn = "r" if self.turn == "y" else "y"

    def col_full(self, col):
        return "" not in self.board[col]

    def winner(self):
        if self._check_winner("y"):
            return "y"
        elif self._check_winner("r"):
            return "r"
        elif self._board_full():
            return "full"
        return None

    def update(self):
        if self.ready_players == 2:
            self.ready = True

    def _board_full(self):
        for col in self.board:
            if "" in col:
                return False
        return True

    def _check_winner(self, color):
        # Check horizontal locations for win
        for c in range(COLS - 3):
            for r in range(ROWS):
                if self.board[c][r] == color and self.board[c + 1][r] == color and self.board[c + 2][r] == color and self.board[c + 3][r] == color:
                    return True

        # Check vertical locations for win
        for c in range(COLS):
            for r in range(ROWS - 3):
                if self.board[c][r] == color and self.board[c][r + 1] == color and self.board[c][r + 2] == color and self.board[c][r + 3] == color:
                    return True

        # Check positively sloped diaganols
        for c in range(COLS - 3):
            for r in range(ROWS - 3):
                if self.board[c][r] == color and self.board[c + 1][r + 1] == color and self.board[c + 2][r + 2] == color and self.board[c + 3][r + 3] == color:
                    return True

        # Check negatively sloped diaganols
        for c in range(COLS - 3):
            for r in range(3, ROWS):
                if self.board[c][r] == color and self.board[c + 1][r - 1] == color and self.board[c + 2][r - 2] == color and self.board[c + 3][r - 3] == color:
                    return True

    def _create_board(self):
        self.board = []
        for col in range(COLS):
            self.board.append([])
            for row in range(ROWS):
                self.board[col].append("")
