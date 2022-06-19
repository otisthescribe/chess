import socket
import time
import os
import chess
import numpy
import pandas as pd
import sys


def make_a_move():
    """
    Asks user for a move and checks if it's legal until the input
    is correct.
    If a user wants to move from A1 to B2, the input should be a1b2.
    :return: legal move (4 characters string)
    """
    while True:
        move = input("Input move: ")
        try:
            if chess.Move.from_uci(move) in board.legal_moves:
                board.push(chess.Move.from_uci(move))
                return move
            else:
                print("Move not legal")
        except Exception:
            # Example: 3 or 5 characters
            print("Wrong input")
            pass


def print_board():
    """
    Clears the terminal and print the current board on it.
    Additional information includes check, checkmate, stalemate and
    insufficient material.
    """
    os.system('clear')
    c = [x.split(' ') for x in str(board).split('\n')]
    c = numpy.array(c)
    brd = pd.DataFrame(c,
                       columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                       index=['8', '7', '6', '5', '4', '3', '2', '1'])
    print(brd)
    if board.is_checkmate():
        print("CHECKMATE!")
    elif board.is_stalemate():
        print("STALEMATE!")
    elif board.is_insufficient_material():
        print("INSUFFICIENT MATERIAL!")
    elif board.is_check():
        print("CHECK!")


# DEFINE CONSTANTS
PORT_MC = 8080  # multicast port to connect on
PORT = 8081  # TCP port to connect/open socket on
mc_group = ('224.0.0.1', PORT_MC)
bufferSize = 1024

# CREATE SOCKET AND SET OPTIONS
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 3)
if len(sys.argv) > 1:
    # optional argument indicating which interface bind the socket on
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, sys.argv[1].encode())

# SENDING MULTICAST REQUEST
sock.sendto(''.encode(), mc_group)
print("Waiting for a server to respond")
data, address = sock.recvfrom(bufferSize)
response = data.decode()
sock.close()

# CREATE THE BOARD AND START A GAME
board = chess.Board()

if response[0] == '0':
    # Player who recieves "0" starts a game (white)
    # Open a TCP socket and start listening
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', PORT))
    sock.listen()
    conn, addr = sock.accept()

    print_board()
    while True:
        # Make a move
        move1 = make_a_move()
        print_board()
        conn.send(move1.encode())
        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
            break
        # Get the opponent's move and apply it to the board
        move2 = conn.recv(bufferSize).decode()
        board.apply_mirror()
        board.push(chess.Move.from_uci(move2))
        board.apply_mirror()
        print_board()
        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
            break

    conn.close()
    sock.close()


else:
    # Player who recieves "1" plays as a second (black)
    r = response.split(',')
    ip = r[1]
    time.sleep(2)  # wait for TCP server player to prepare
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, PORT))

    board.apply_mirror()
    print_board()
    while True:
        # Get the opponent's move and apply it to the board
        move2 = sock.recv(bufferSize)
        move2 = move2.decode()
        board.apply_mirror()
        board.push(chess.Move.from_uci(move2))
        board.apply_mirror()
        print_board()
        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
            break
        # Make a move
        move1 = make_a_move()
        print_board()
        sock.send(move1.encode())
        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
            break

    sock.close()

print_board()
print(board.outcome())
