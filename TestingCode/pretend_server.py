import socket
import pickle
import pygame

pygame.init()

print("Server started...")
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)

server_ip = '127.0.0.1'
server_port = 7000

def controller():
    # global buffer

    joystick = {}
    done = False
    while not done:
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True  # Flag that we are done so we exit this loop.

                if event.type == pygame.JOYBUTTONDOWN:
                    # print("BUTTON DOWN")
                    buffer = "Joystick button pressed."
        
                if event.type == pygame.JOYBUTTONUP:
                    buffer = "Joystick button released."

                # Handle hotplugging
                if event.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(event.device_index)
                    joystick[joy.get_instance_id()] = joy
                    buffer = "Joystick {} connencted".format(joy.get_instance_id())

                if event.type == pygame.JOYDEVICEREMOVED:
                    del joystick[event.instance_id]
                    buffer = "Joystick {} disconnected".format(event.instance_id)
                
                # server stuff
                x_as_bytes = pickle.dumps(buffer)
                server.sendto((x_as_bytes), (server_ip, server_port))

        except Exception as e:
            print(e)

if __name__ == "__main__":
    controller()
    pygame.quit()