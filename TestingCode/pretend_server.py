import socket
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)

server_ip = '127.0.0.1'
server_port = 6666

while True:
    buffer="hello world"
    x_as_bytes = pickle.dumps(buffer)

    s.sendto((x_as_bytes), (server_ip, server_port))