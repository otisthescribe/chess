import socket
import struct
import chess

# DEFINE CONSTANTS
PORT = 8080
mc_group = ('224.3.29.71', PORT)
bufferSize = 1024

# CREATE SOCKET AND SET OPTIONS
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)


# SENDING MULTICAST REQUEST
sock.sendto(''.encode(), mc_group)
print("Waiting for a server to response")
data, address = sock.recvfrom(bufferSize)
print(f"{data.decode()} from {address}")
