import socket
import time
import struct
import os
import chess
import numpy
import pandas as pd

# DEFINE CONSTANTS
PORT = 8080
PORT2 = 8081
mc_group = ('224.3.29.71', PORT)
bufferSize = 1024

# CREATE SOCKET AND SET OPTIONS
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

# SENDING MULTICAST REQUEST
sock.sendto(''.encode(), mc_group)
print("Waiting for a server to respond")
data, address = sock.recvfrom(bufferSize)

response = data.decode()
sock.close()

board = chess.Board()
clear = lambda: os.system('clear')


def wykonanie_ruchu():
    while True:
        polecenie = input("Input move: ")
        try:
            if chess.Move.from_uci(polecenie) in board.legal_moves:
                board.push(chess.Move.from_uci(polecenie))
                return polecenie
        except Exception:
            print("Zle wejscie")
            pass
    # polecenie "Pole1Pole2" ruch z a1 na b2 to polecenie = "a1b2"


def wypisanie():
    c = [x.split(' ') for x in str(board).split('\n')]
    c = numpy.array(c)
    df2 = pd.DataFrame(c,
                       columns=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                       index=['8', '7', '6', '5', '4', '3', '2', '1'])
    print(df2)


if response[0] == '0':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', PORT2))
    sock.listen()
    conn, addr = sock.accept()

    clear()
    wypisanie()
    while True:
        ruch1 = wykonanie_ruchu()
        clear()
        wypisanie()
        conn.send(ruch1.encode())
        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
            break
        ruch2 = conn.recv(bufferSize).decode()
        board.push(chess.Move.from_uci(ruch2))
        clear()
        wypisanie()
        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
            break

    conn.close()
    sock.close()


else:
    x = response.split(',')
    ip = x[1]
    time.sleep(2)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, PORT2))

    clear()
    wypisanie()
    while True:
        ruch2 = sock.recv(bufferSize)
        ruch2 = ruch2.decode()
        board.push(chess.Move.from_uci(ruch2))
        clear()
        wypisanie()
        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
            break
        ruch1 = wykonanie_ruchu()
        clear()
        wypisanie()
        sock.send(ruch1.encode())
        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
            break

    sock.close()

clear()
wypisanie()
print(board.outcome())


