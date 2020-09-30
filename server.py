import socket, threading, pickle
from board import Board
from constants import HEADER, PORT, FORMAT, DISCONNECT

"""
How messages will be sent:

Client sends:
"get" - server sends board
"reset" - server resets the board
"ready" - server readies board
int(0 - 6) - server inserts in the column
"""


SERVER = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))


def create_open_games(max_games):
    open_games = []
    for i in range(max_games):
        open_games.append(i)
        open_games.append(i)
    return open_games


MAX_GAMES = int(input("Max amount of games possible: "))
open_games = create_open_games(MAX_GAMES)
games = {}  # game_id : board
firstplayer_colors = []  # game_id as index - "r" or "y"
for i in set(open_games):
    games[i] = Board()
    firstplayer_colors.append(0)


class Client:
    def __init__(self, conn, addr, game_id, player_id):
        self.conn, self.addr, self.game_id, self.player_id = conn, addr, game_id, player_id
        self.color = "r" if player_id % 2 == 0 else "y"
        self._communicate()

    def _communicate(self):
        global open_games
        self._send(self.color)
        connected = True
        while connected:
            mesg = self._receive()
            if self.game_id in games:
                try:
                    if mesg.isdigit():
                        games[self.game_id].insert(int(mesg))
                    elif mesg == "reset":
                        games[self.game_id] = Board()
                        games[self.game_id].ready = True
                    elif mesg == "ready":
                        games[self.game_id].ready_players += 1
                    elif mesg == DISCONNECT:
                        connected = False
                    if mesg not in (DISCONNECT, "ready"):
                        self._send_board()
                except:
                    print("[SERVER] Communication with client is not working")
            else:
                break
        print(f"[DISCONNECT] Player {self.player_id} has left game {self.game_id}")
        open_games.append(self.game_id)
        games[self.game_id] = Board()
        if open_games.count(self.game_id) == 2:
            games[self.game_id].ready_players = 0
        elif open_games.count(self.game_id) == 1:
            games[self.game_id].ready_players = 1
        self.conn.close()

    def _receive(self):
        mesg_len = self.conn.recv(HEADER).decode(FORMAT)
        if mesg_len:
            return self.conn.recv(int(mesg_len)).decode(FORMAT)
        else:
            return None

    def _send(self, mesg):
        mesg_len = str(len(mesg)).encode(FORMAT)
        mesg_len += b" " * (HEADER - len(mesg_len))

        self.conn.send(mesg_len)
        self.conn.send(mesg.encode(FORMAT))

    def _send_board(self):
        games[self.game_id].update()
        self.conn.send(pickle.dumps(games[self.game_id]))


def ready_games():
    for game_id in range(MAX_GAMES):
        if game_id not in open_games:
            games[game_id].update()


def accept():
    global open_games, firstplayer_colors
    print(f"Server listening on {SERVER}")
    server.listen(MAX_GAMES*2)
    player_id = 0  # 0 means Red, 1 means Yellow

    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] Address: {addr}, has connected!")
        print(f"{threading.activeCount()} active connections")

        # open_games.sort(key=lambda x: open_games.count(x))
        open_games = sorted(open_games, key=lambda x: open_games.count(x))
        game_id = open_games.pop(0)
        if open_games.count(game_id)
        threading.Thread(target=Client, args=(conn, addr, game_id, player_id)).start()
        print(f"Player {player_id} has joined game {game_id}")
        ready_games()
        player_id += 1


print("Server is starting...")
accept()
