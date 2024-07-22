import tkinter
root = tkinter.Tk()

# specify resolutions of both windows
w0, h0 = 1920, 1080
w1, h1 = 1920, 1080

# set up a window for first display, if wanted  
win0 = tkinter.Toplevel()
win0.geometry(f"{w0}x{h0}+0+0")

# set up window for second display with fullscreen 
win1 = tkinter.Toplevel()
win1.geometry(f"{w1}x{h1}+{w0}+0") # <- this is the key, offset to the right by w0
win1.attributes("-fullscreen", True)