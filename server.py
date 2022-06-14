from email import message
from os import fork
import socket
import struct
import chess
import os

# DEFINING CONSTANTS
PORT = 8080
bufferSize = 1024
multicast = '224.3.29.71'
mc_group = (multicast, PORT)

# CREATING SOCKET AND SETTING OPTIONS
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', PORT))
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
print("UDP server up and listening")

# JOIN THE MULTICAST GROUP
group = socket.inet_aton(multicast)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


while True:

    # Get the first user
    data1, address1 = sock.recvfrom(bufferSize)
    print("First user joined")
    # Get the second user
    data2, address2 = sock.recvfrom(bufferSize)
    print("Second user joined")
    # Create new process that will host a game
    pid = os.fork()

    if pid > 0:
        continue
        
    else:
        mes = "New game created, but no funcionality yet"
        sock.sendto(mes.encode(), address1)
        sock.sendto(mes.encode(), address2)
        break




# # ECHO MECHANISM
# print("Waiting to receive message")
# while True:
#     try:
#         data, address = sock.recvfrom(bufferSize)
#         print(f"Received '{data.decode()}' from {address}")
#         sock.sendto(data, address)
#     except Exception:
#         continue
