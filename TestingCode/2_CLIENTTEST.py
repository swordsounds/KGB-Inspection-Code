import pygame, socket, pickle

HEADER = 2048
PORT = 8000
FORMAT = 'utf-8'
DC_MESSAGE = "!DISCONNECT"
SERVER = "192.168.0.23"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = str(msg).encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b" " * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


info = {
        "dpad_up": 0,
        "dpad_down": 0,
        "dpad_left": 0,
        "dpad_right": 0,
        }
pygame.init()
def main():
    joysticks = {}
    done = False
    while not done:
        # Event processing step.
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True  # Flag that we are done so we exit this loop.

                # Handle hotplugging
                if event.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(event.device_index)
                    joysticks[joy.get_instance_id()] = joy
                    print(f"Joystick connected")

                if event.type == pygame.JOYDEVICEREMOVED:
                    del joysticks[event.instance_id]
                    print(f"Joystick disconnected")

                if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick pressed")
            # For each joystick:
            for joystick in joysticks.values():
                # axes = joystick.get_numaxes()
                # for i in range(axes):                 
                #     axis = joystick.get_axis(i)
                    # print(f"Axis {i} value: {axis:>6.3f}")
                
                for buttons in range(11, 15):
                    
                        button_mapping = {11: 'dpad_up',
                                        12: 'dpad_down',
                                        13: 'dpad_left',
                                        14: 'dpad_right'
                                        }
                        value = joystick.get_button(buttons)
                        info[button_mapping[buttons]] = value               
        except Exception as e:
            print(e)
        send(info)
if __name__ == "__main__":
    main()
    send(DC_MESSAGE)
    pygame.quit()