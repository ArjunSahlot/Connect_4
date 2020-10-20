import pygame, os, pickle
import tkinter as tk
import socket
from Connect_4.constants import *
from Connect_4.board import Board
pygame.init()


SERVER = input("Server IP: ")
# SERVER = socket.gethostbyname(socket.gethostname())  # Use only when running client on same machine as server

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
except:
    input("Unable to connect.")
    exit()

screen_width = tk.Tk().winfo_screenwidth()
screen_height = tk.Tk().winfo_screenheight()

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screen_width//2-WIDTH//2, screen_height//2-HEIGHT//2)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4, By: Arjun Sahlot")
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "icon.png")))
FONT = pygame.font.SysFont("comicsans", RADIUS*2-6)


def receive_obj():
    return pickle.loads(client.recv(4096))


def receive():
    mesg_len = client.recv(HEADER).decode(FORMAT)
    if mesg_len:
        return client.recv(int(mesg_len)).decode(FORMAT)
    else:
        return None


def send(mesg):
    mesg_len = str(len(mesg)).encode(FORMAT)
    mesg_len += b" " * (HEADER - len(mesg_len))

    client.send(mesg_len)
    client.send(mesg.encode(FORMAT))


def draw_window(win, board, winner, color, anim_time):
    win.fill(BLACK)
    win.fill(BLUE, (0, RADIUS * 2, WIDTH, HEIGHT - RADIUS * 2))
    pygame.draw.circle(win, RED if color == "r" else YELLOW, (pygame.mouse.get_pos()[0], RADIUS), RADIUS)
    pygame.draw.rect(win, RED if color == "r" else YELLOW, (15, 15, 30, 30))
    board.draw(win, anim_time)
    if winner or board.turn != color and board.ready:
        if winner == "r":
            text = FONT.render("You Win!" if color == "r" else "You Lost...", 1, RED if color == "r" else YELLOW)
        elif winner == "y":
            text = FONT.render("You Win!" if color == "y" else "You Lost...", 1, RED if color == "r" else YELLOW)
        elif winner == "full":
            text = FONT.render("The Board is Full.", 1, WHITE)
        else:
            mult = anim_time//200%4
            text = FONT.render("Waiting for opponent" + "."*mult, 1, WHITE)
        win.blit(text, (WIDTH//2 - text.get_width()//2, RADIUS - text.get_height()//2))
        pygame.display.update()


def mouse_to_col(mouseX):
    return mouseX // int(WIDTH/COLS)


def board_full(board):
    for col in board.board:
        if "" in col:
            return False
    return True


def main(win, color):
    run = True
    anim_time = 0
    send("get")
    board = receive_obj()
    while run:
        anim_time += 1
        winner = board.winner()
        draw_window(win, board, winner, color, anim_time)
        if winner:
            pygame.time.delay(1500)
            send("reset")
            print("[GAME] Resetting board")
            board = receive_obj()
        else:
            send("get")
            board = receive_obj()
        mouseX = pygame.mouse.get_pos()[0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                send(DISCONNECT)
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.turn == color:
                    send(str(mouse_to_col(mouseX)))
                    board = receive_obj()

        pygame.display.update()


def menu(win):
    run = True
    win.fill(BLACK)
    asdf = FONT.render("Click to play!", 1, WHITE)
    win.blit(asdf, (WIDTH//2 - asdf.get_width()//2, HEIGHT//2 - asdf.get_height()//2))
    pygame.display.update()
    color = receive()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                send(DISCONNECT)
                print("[GAME] You got disconnected from the game")
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                send("ready")
                print("[GAME] You are ready to play!")
    main(win, color)


while True:
    menu(WINDOW)
