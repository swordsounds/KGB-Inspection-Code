import socket
import pickle
import time
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)

server_ip = '127.0.0.1'
server_port = 7000

while True:
    buffer="hello world"
    x_as_bytes = pickle.dumps(buffer)

    time.sleep(1)
    print("Server is running")
    s.sendto((x_as_bytes), (server_ip, server_port))