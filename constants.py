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

ROWS, COLS = 6, 7
SQUARE_SIZE = 120

WIDTH, HEIGHT = COLS*SQUARE_SIZE, (ROWS+1)*SQUARE_SIZE

RADIUS = int(SQUARE_SIZE/2 - 5)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (30, 30, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

HEADER = 1024
PORT = 5050
FORMAT = "utf-8"
DISCONNECT = "quit"
