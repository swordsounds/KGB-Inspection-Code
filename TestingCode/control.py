from pyPS4Controller.controller import Controller

# Translate controller input into motor output values
def transf(raw):
    temp = (raw+32767)/65534
    # Filter values that are too weak for the motors to move
    if abs(temp) < 0.25:
        return 0
    # Return a value between 0.3 and 1.0
    else:
        return round(temp, 1)

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
    
    def on_R2_press(self, value):
        # 'value' becomes 0 or a float between 0.3 and 1.0
        value = transf(value)
        print(f"R2 {value}")
    
    def on_R2_release(self):
        print(f"R2 FREE")
    
    def on_L2_press(self, value):
        # 'value' becomes 0 or a float between -1.0 and -0.3
        value = -transf(value)
        print(f"L2 {value}")
    
    def on_L2_release(self):
        print(f"L2 FREE")
    
    # Press OPTIONS (=START) to stop and exit
    def on_options_press(self):
        print("\nExiting (START)")
        exit(1)


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()