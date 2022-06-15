# CHESS

Server-client based chess game with automatic pairing of 
players. Server runs on UDP port 8080 and listen for 
multicast requests. If two players are ready, they are paired.
Server sends the ip address of one client to another and then 
clients create the TCP connection between themselves.


## Instalation
python3 setup.py install

## Usage
First step is to run the server script. 
It will run as a daemon and listen for UDP multicast 
requests on port 8080. Information and errors are sent to 
syslog.

### Server
python3 server.py

### Client
python3 client.py