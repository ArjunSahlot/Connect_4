import pygame, os
from constants import *
import tkinter as tk
pygame.init()


root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screen_width//2-WIDTH//2, screen_height//2-HEIGHT//2)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4, By: Arjun Sahlot")
# pygame.display.set_caption()
FONT = pygame.font.SysFont("comicsans", RADIUS*2-6)


def create_board():
    board = []
    for col in range(COLS):
        board.append([])
        for row in range(ROWS):
            board[col].append("")

    return board


def draw_board(win, board):
    for col in range(len(board)):
        for row in range(len(board[col])):
            if board[col][row] == "":
                pygame.draw.circle(win, BLACK, (9*(col+1) + RADIUS + RADIUS*2*col, RADIUS*3 + 9*(row+1) + RADIUS*2*row + 5), RADIUS)
            else:
                pygame.draw.circle(win, YELLOW if board[col][row] == "y" else RED, (9*(col+1) + RADIUS + RADIUS*2*col, RADIUS*3 + 9*(row+1) + RADIUS*2*row + 5), RADIUS)


def draw_window(win, board, winner):
    win.fill(BLACK)
    win.fill(BLUE, (0, RADIUS * 2, WIDTH, HEIGHT - RADIUS * 2))
    draw_board(win, board)
    if winner:
        if winner == "r":
            text = FONT.render("Red Wins!", 1, RED)
        elif winner == "y":
            text = FONT.render("Yellow Wins!", 1, YELLOW)
        elif winner == "full":
            text = FONT.render("The Board is Full.", 1, WHITE)
        win.blit(text, (WIDTH//2 - text.get_width()//2, RADIUS - text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)
        if winner == "full":
            return "reset"
        exit()


def mouse_to_col(mouseX):
    return mouseX // int(WIDTH/COLS)


def insert(col, board, color):
    for pos in range(ROWS-1, -1, -1):
        if board[col][pos] == "":
            board[col][pos] = color
            break
    return board


def col_full(col, board):
    return "" not in board[col]


def check_winner(board, color):
    # Check horizontal locations for win
    for c in range(COLS - 3):
        for r in range(ROWS):
            if board[c][r] == color and board[c + 1][r] == color and board[c + 2][r] == color and board[c + 3][r] == color:
                return True

    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[c][r] == color and board[c][r + 1] == color and board[c][r + 2] == color and board[c][r + 3] == color:
                return True

    # Check positively sloped diaganols
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if board[c][r] == color and board[c + 1][r + 1] == color and board[c + 2][r + 2] == color and board[c + 3][r + 3] == color:
                return True

    # Check negatively sloped diaganols
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if board[c][r] == color and board[c + 1][r - 1] == color and board[c + 2][r - 2] == color and board[c + 3][r - 3] == color:
                return True


def red_win(board):
    return check_winner(board, "r")


def yellow_win(board):
    return check_winner(board, "y")


def board_full(board):
    for col in board:
        if "" in col:
            return False
    return True


def main(win):
    board = create_board()
    turn = "r"
    winner = None
    run = True
    while run:
        mouseX = pygame.mouse.get_pos()[0]
        if draw_window(win, board, winner) == "reset":
            board = create_board()
        winner = None
        pygame.draw.circle(win, RED if turn == "r" else YELLOW, (mouseX, RADIUS), RADIUS)
        if red_win(board):
            winner = "r"
        elif yellow_win(board):
            winner = "y"
        elif board_full(board):
            winner = "full"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseCol = mouse_to_col(mouseX)
                if not col_full(mouseCol, board):
                    board = insert(mouseCol, board, turn)
                    turn = "r" if turn == "y" else "y"

        pygame.display.update()


main(WINDOW)
