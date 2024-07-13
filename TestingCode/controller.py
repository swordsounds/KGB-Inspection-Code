import pygame

pygame.init()

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
                
                if event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released.")

                # Handle hotplugging
                if event.type == pygame.JOYDEVICEADDED:
                    print(f"Joystick connencted")

                if event.type == pygame.JOYDEVICEREMOVED:
                    del joysticks[event.instance_id]
                    print(f"Joystick disconnected")

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
                
                for i in range(axes):
                    axis = joystick.get_axis(i)
                    print(f"Axis {i} value: {axis:>6.3f}")
                

                buttons = joystick.get_numbuttons()
                print(f"Number of buttons: {buttons}")
                

                for i in range(buttons):
                    button = joystick.get_button(i)
                    print(f"Button {i:>2} value: {button}")
              
        except Exception as e:
            print(e)
        clock.tick(30)

if __name__ == "__main__":
    controller()
    pygame.quit()