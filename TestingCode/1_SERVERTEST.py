import socket, pickle

SERVER_CONTROL_BOX = '192.168.0.23'
CONTROL_BOX_PORT = 10000

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2048)
server.bind((SERVER_CONTROL_BOX, CONTROL_BOX_PORT))

while True:

    data_from_control_box = server.recvfrom(2048)
    data_from_control_box = data_from_control_box[0]
    data = pickle.loads(data_from_control_box)
    print(data)