import csv
import pygame

# fieldnames = ['dpad_up', 'dpad_down', 'dpad_left', 'dpad_right']

# with open('scrapthis.csv', 'w') as csv_file:
#         csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#         csv_writer.writeheader()

pygame.init()

def controller():
    # global buffer

    clock = pygame.time.Clock()
    joysticks = {}
    info = {
                "dpad_up": 0,
                "dpad_down": 0,
                "dpad_left": 0,
                "dpad_right": 0,
            }
    done = False
    while not done:
        # with open('data.csv', 'w') as csv_file:
        #     csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            
            
        #     csv_writer.writerow(info)
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True  # Flag that we are done so we exit this loop.

                # Handle hotplugging
                if event.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(event.device_index)
                    joysticks[joy.get_instance_id()] = joy
                    print(f"Joystick connencted")

                if event.type == pygame.JOYDEVICEREMOVED:
                    del joysticks[event.instance_id]
                    print(f"Joystick disconnected")
                
            # For each joystick:
            for joystick in joysticks.values():
                axes = joystick.get_numaxes()
                
                for i in range(axes):                 
                    axis = joystick.get_axis(i)
                    # print(f"Axis {i} value: {axis:>6.3f}")
            

                for buttons in range(11, 15):
                    button_mapping = {11: 'dpad_up',
                                      12: 'dpad_down',
                                      13: 'dpad_left',
                                      14: 'dpad_right'
                                      }
                    value = joystick.get_button(buttons)
                    info[button_mapping[buttons]] = value
                    print(info)
                    # print(f"{button_mapping[buttons]} value: {value}")
            clock.tick(30)      
        except Exception as e:
            print(e)
        

if __name__ == "__main__":
    controller()
    pygame.quit()