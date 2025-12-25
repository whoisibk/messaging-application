import socket

# retrieve ip address of server
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090

# configure the socket server to be of type internet and TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind server to an ip add. and port
server.bind(HOST, PORT)
server.listen()


hostInfo = (HOST, PORT)


while True:
    server.accept(hostInfo)
