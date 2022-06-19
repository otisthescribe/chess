import socket
import struct
import syslog
import os
import signal
import sys

# Open syslog - only in Linux

syslog.openlog()

# DEMONIZE THE PROCESS

try:
    pid = os.fork()
    if pid > 0:
        sys.exit(0)
except Exception:
    syslog.syslog(f"Fork failed")
    sys.exit(0)

os.setsid()
signal.signal(signal.SIGHUP, signal.SIG_IGN)

try:
    pid = os.fork()
    if pid > 0:
        sys.exit(0)
except Exception:
    syslog.syslog(f"Fork failed")
    sys.exit(0)

os.chdir("/")
os.umask(0)
f = open('/dev/null', 'w')
sys.stdout = f
sys.stdin = f
sys.stderr = f


# DEFINING CONSTANTS
PORT_MC = 8080  # port for multicast UDP server
bufferSize = 1024
multicast = '224.0.0.1'
mc_group = (multicast, PORT_MC)


# CREATING SOCKET AND SETTING OPTIONS
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) > 1:
    # optional argument indicating which interface bind the socket on
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, sys.argv[1].encode())
sock.bind((multicast, PORT_MC))

# JOIN THE MULTICAST GROUP
mreq = struct.pack('4sl', socket.inet_aton(multicast), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

syslog.syslog("UDP multicast server up and listening")

while True:
    # Get the first user
    # Send "0" - open a TCP socket and listen for incoming connections
    data1, address1 = sock.recvfrom(bufferSize)
    sock.sendto("0".encode(), address1)

    # Get the second user
    # Send "1" + IP ADD - connect with a TCP socket with IP ADDRESS
    data2, address2 = sock.recvfrom(bufferSize)
    sock.sendto(f"1,{address1[0]}".encode(), address2)

    syslog.syslog(f"User ({address1[0]}) plays with user ({address2[0]})")
