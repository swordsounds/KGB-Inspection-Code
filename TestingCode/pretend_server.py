import socket, pickle, pygame

pygame.init()

print("Server started...")
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)

server_ip = '127.0.0.1'
server_port = 8000

def controller():
    # global buffer

    clock = pygame.time.Clock()
    joysticks = {}

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
                    print("Joystick button pressed.")
                    if event.button == 0:
                        joystick = joysticks[event.instance_id]
                        if joystick.rumble(0, 0.7, 500):
                            print(f"Rumble effect played on joystick {event.instance_id}")

                if event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released.")

                # Handle hotplugging
                if event.type == pygame.JOYDEVICEADDED:
                    # This event will be generated when the program starts for every
                    # joystick, filling up the list without needing to create them manually.
                    joy = pygame.joystick.Joystick(event.device_index)
                    joysticks[joy.get_instance_id()] = joy
                    print(f"Joystick {joy.get_instance_id()} connencted")

                if event.type == pygame.JOYDEVICEREMOVED:
                    del joysticks[event.instance_id]
                    print(f"Joystick {event.instance_id} disconnected")

            # Get count of joysticks.
            joystick_count = pygame.joystick.get_count()

            print(f"Number of joysticks: {joystick_count}")
        

            # For each joystick:
            for joystick in joysticks.values():
                jid = joystick.get_instance_id()

                print(f"Joystick {jid}")
            

                # Get the name from the OS for the controller/joystick.
                name = joystick.get_name()
                print(f"Joystick name: {name}")

                guid = joystick.get_guid()
                print(f"GUID: {guid}")

                power_level = joystick.get_power_level()
                print(f"Joystick's power level: {power_level}")

                # Usually axis run in pairs, up/down for one, and left/right for
                # the other. Triggers count as axes.
                axes = joystick.get_numaxes()
                print(f"Number of axes: {axes}")
                

                for i in range(axes):
                    axis = joystick.get_axis(i)
                    print(f"Axis {i} value: {axis:>6.3f}")
                

                buttons = joystick.get_numbuttons()
                print(f"Number of buttons: {buttons}")
                

                for i in range(buttons):
                    button = joystick.get_button(i)
                    print(f"Button {i:>2} value: {button}")
                

                hats = joystick.get_numhats()
                print(f"Number of hats: {hats}")
                

                # Hat position. All or nothing for direction, not a float like
                # get_axis(). Position is a tuple of int values (x, y).
                for i in range(hats):
                    hat = joystick.get_hat(i)
                    print(f"Hat {i} value: {str(hat)}")
                

                    
                    # server stuff
                    x_as_bytes = pickle.dumps(buffer)
                    server.sendto((x_as_bytes), (server_ip, server_port))
                
        except Exception as e:
            print(e)
        clock.tick(30)
if __name__ == "__main__":
    controller()
    pygame.quit()