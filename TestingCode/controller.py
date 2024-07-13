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

    # def __init__(self):
    #     self.controller()

    # def controller(self):
    #     pygame.init()
    #     joysticks = {}

    #     done = False
    #     while not done:
    #         # Event processing step.
    #         try:
    #             for event in pygame.event.get():
    #                 if event.type == pygame.QUIT:
    #                     done = True  # Flag that we are done so we exit this loop.

    #                 # Handle hotplugging
    #                 if event.type == pygame.JOYDEVICEADDED:
    #                     joy = pygame.joystick.Joystick(event.device_index)
    #                     joysticks[joy.get_instance_id()] = joy
    #                     print(f"Joystick connected")

    #                 if event.type == pygame.JOYDEVICEREMOVED:
    #                     del joysticks[event.instance_id]
    #                     print(f"Joystick disconnected")

    #             # For each joystick:
    #             for joystick in joysticks.values():
    #                 # axes = joystick.get_numaxes()
    #                 # for i in range(axes):                 
    #                 #     axis = joystick.get_axis(i)
    #                     # print(f"Axis {i} value: {axis:>6.3f}")
                    
    #                 for buttons in range(11, 15):
                        
    #                         button_mapping = {11: 'dpad_up',
    #                                         12: 'dpad_down',
    #                                         13: 'dpad_left',
    #                                         14: 'dpad_right'
    #                                         }
    #                         value = joystick.get_button(buttons)
    #                         self.info[button_mapping[buttons]] = value
                          
    #         except Exception as e:
    #             print(e)
    #         self.send_msg()

            # server stuff
    def send_msg(self):        
            x_as_bytes = pickle.dumps(self.info)
            self.server.sendto((x_as_bytes), (self.server_ip, self.server_port))

if __name__ == "__main__":
    x = Server()
    x()
    pygame.quit()