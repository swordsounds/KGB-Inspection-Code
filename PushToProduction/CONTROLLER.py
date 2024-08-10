import socket, pickle, pygame, time # type: ignore

pygame.init()

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2048)

SERVER = '192.168.0.19'
CMDPORT = 8000 

info = {
        "CRAWL": '',
        "PTZ_MOVEMENT": ''
        }


def controller():
    joysticks = {}

    time.sleep(2)

    done = False
    while not done:
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick button pressed.")
                    # ROBOT.forward(speed=1)
                    send_msg()

                if event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released.")
                    # ROBOT.stop()
                    send_msg()

                if event.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(event.device_index)
                    joysticks[joy.get_instance_id()] = joy
                    print(f"Joystick connected")

                if event.type == pygame.JOYDEVICEREMOVED:
                    del joysticks[event.instance_id]
                    print(f"Joystick disconnected")

             
            for joystick in joysticks.values():

                x_axis_value_left = round(joystick.get_axis(0), 1)
                y_axis_value_left = round(joystick.get_axis(1), 1)

                x_axis_value_right = round(joystick.get_axis(3), 1)
                y_axis_value_right = round(joystick.get_axis(4), 1)

                if x_axis_value_left == 1:
                    info['PTZ_MOVEMENT'] = ''
                    info['CRAWL'] = 'RIGHT'
                    x_as_bytes = pickle.dumps(info)
                    server.sendto((x_as_bytes), (SERVER, CMDPORT))

                elif x_axis_value_left == -1:
                    info['PTZ_MOVEMENT'] = ''
                    info['CRAWL'] = 'LEFT'
                    x_as_bytes = pickle.dumps(info)
                    server.sendto((x_as_bytes), (SERVER, CMDPORT))

                elif y_axis_value_left == -1:
                    info['PTZ_MOVEMENT'] = ''
                    info['CRAWL'] = 'FORW'
                    x_as_bytes = pickle.dumps(info)
                    server.sendto((x_as_bytes), (SERVER, CMDPORT))
                
                elif y_axis_value_left == 1:
                    info['PTZ_MOVEMENT'] = ''
                    info['CRAWL'] = 'BACK'
                    x_as_bytes = pickle.dumps(info)
                    server.sendto((x_as_bytes), (SERVER, CMDPORT))
                


                if x_axis_value_right == 1:
                    info['CRAWL'] = 'STOP'
                    info['PTZ_MOVEMENT'] = 'RIGHT'
                    x_as_bytes = pickle.dumps(info)
                    server.sendto((x_as_bytes), (SERVER, CMDPORT))

                elif x_axis_value_right == -1:
                    info['CRAWL'] = 'STOP'
                    info['PTZ_MOVEMENT'] = 'LEFT'
                    x_as_bytes = pickle.dumps(info)
                    server.sendto((x_as_bytes), (SERVER, CMDPORT))

                elif y_axis_value_right == -1:
                    info['CRAWL'] = 'STOP'
                    info['PTZ_MOVEMENT'] = 'UP'
                    x_as_bytes = pickle.dumps(info)
                    server.sendto((x_as_bytes), (SERVER, CMDPORT))
                
                elif y_axis_value_right == 1:
                    info['CRAWL'] = 'STOP'
                    info['PTZ_MOVEMENT'] = 'DOWN'
                    x_as_bytes = pickle.dumps(info)
                    server.sendto((x_as_bytes), (SERVER, CMDPORT))
                

                # for buttons in range(0, 4):
                    
                #         button_mapping = {0: 'dpad_up',
                #                         1: 'dpad_down',
                #                         2: 'dpad_left',
                #                         3: 'dpad_right'
                #                         }
                #         value = joystick.get_button(buttons)
                #         info[button_mapping[buttons]] = value
                       
                # hats = joystick.get_numhats()
                # for i in range(hats):
                #     hat = joystick.get_hat(i)
                #     print(f"Hat {i} value: {str(hat)}")

# server stuff
def send_msg(): 
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

if __name__ == "__main__":
    print("Server started...")
    controller()
    pygame.quit()
