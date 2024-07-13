import socket, pickle
import threading

HEADER = 2048
PORT = 8000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR= (SERVER, PORT)
FORMAT = 'utf-8'
DC_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"Connection {addr}")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DC_MESSAGE:
                connected = False
        conn.sendto('Ping'.encode(FORMAT), (SERVER, PORT))
    conn.close()

def start():
    server.listen()
    print(f"Server Listening... {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Connections: {threading.active_count() - 1}")
        
print("Starting server...")
start()