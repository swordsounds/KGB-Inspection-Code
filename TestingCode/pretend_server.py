import socket, pickle, pygame

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2048)

SERVER = '127.0.0.1'
CMDPORT = 8000 

info = {
            "dpad_up": 0,
            "dpad_down": 0,
            "dpad_left": 0,
            "dpad_right": 0,
        }

def controller():
    pygame.init()
    joysticks = {}

    done = False
    while not done:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick button pressed.")

                if event.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(event.device_index)
                    joysticks[joy.get_instance_id()] = joy
                    print(f"Joystick connected")

                if event.type == pygame.JOYDEVICEREMOVED:
                    del joysticks[event.instance_id]
                    print(f"Joystick disconnected")

            for joystick in joysticks.values():
                # axes = joystick.get_numaxes()
                # for i in range(axes):                 
                #     axis = joystick.get_axis(i)
                    # print(f"Axis {i} value: {axis:>6.3f}")
                
                
                for buttons in range(11, 15): #on pi, dpad is hat
                    
                        button_mapping = {11: 'dpad_up',
                                        12: 'dpad_down',
                                        13: 'dpad_left',
                                        14: 'dpad_right'
                                        }
                        value = joystick.get_button(buttons)
                        info[button_mapping[buttons]] = value
                        
        except Exception as e:
            print(e)
        send_msg()

# server stuff
def send_msg(): 
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

if __name__ == "__main__":
    print("Server started...")
    controller()
    pygame.quit()