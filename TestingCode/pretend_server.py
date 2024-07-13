import socket, pickle, pygame

class Server:
    print("Server started...")
    info = {
                "dpad_up": 0,
                "dpad_down": 0,
                "dpad_left": 0,
                "dpad_right": 0,
            }

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)

    server_ip = '127.0.0.1'
    server_port = 8000
    
    # server stuff
    def send_msg(self):        
            x_as_bytes = pickle.dumps(self.info)
            self.server.sendto((x_as_bytes), (self.server_ip, self.server_port))

if __name__ == "__main__":
    x = Server()
    x()
    pygame.quit()