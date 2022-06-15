import socket
import struct
import sys
import syslog
import os
import signal

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
syslog.syslog("UDP server up and listening")

# JOIN THE MULTICAST GROUP
group = socket.inet_aton(multicast)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    # Get the first user
    data1, address1 = sock.recvfrom(bufferSize)
    sock.sendto("0".encode(), address1)
    # Get the second user
    data2, address2 = sock.recvfrom(bufferSize)
    sock.sendto(f"1,{address1[0]}".encode(), address2)

    syslog.syslog(f"User ({address1[0]}) plays with user ({address2[0]})")
