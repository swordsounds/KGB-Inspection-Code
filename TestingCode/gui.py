import cv2
import customtkinter
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime

class MyVideoCapture:
    def __init__(self, video_source):
        self.vid = cv2.VideoCapture(video_source)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        ret, frame = self.vid.read()
        return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
       
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master):
        super().__init__(master)

        self.add("Video/Pic")
        self.add("Tether")

        # video buttons

        self.button = customtkinter.CTkButton(master=self.tab("Video/Pic"), command=None, text="Rec.")
        self.button.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.button = customtkinter.CTkButton(master=self.tab("Video/Pic"), command=None, text="Stop Rec.")
        self.button.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.button = customtkinter.CTkButton(master=self.tab("Video/Pic"), command=None, text="Take Pic.")
        self.button.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        # tether buttons

        self.button = customtkinter.CTkButton(master=self.tab("Tether"), command=None, text="Extend Tether")
        self.button.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.button = customtkinter.CTkButton(master=self.tab("Tether"), command=None, text="Stop Tether")
        self.button.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.button = customtkinter.CTkButton(master=self.tab("Tether"), command=None, text="Retract Tether")
        self.button.grid(row=2, column=0, padx=20, pady=20, sticky="ew")



class App(customtkinter.CTk):
    customtkinter.set_appearance_mode("dark")

    def __init__(self):
        super().__init__()

        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        geometry = str(width) + "x" + str(height)
        self.geometry(geometry)

        self.title("Control Panel")
        self.wm_iconbitmap(default=None)
        self.minsize(300, 200)

        # 8x8 grid system

        self.grid_rowconfigure(tuple(range(9)), weight=1)
        self.grid_columnconfigure(tuple(range(9)), weight=1)

        # time display 

        self.time = customtkinter.CTkTextbox(master=self,height=10, font=("", 20))
        self.time.grid(row=0, column=0, padx=0, pady=20, sticky=None)
        self.time.insert("0.0", 'CURRENTTIME')

        # display placeholder 

        self.video_feed = customtkinter.CTkTextbox(master=self, font=("", 25))
        self.video_feed.grid(row=1, column=3, rowspan=8, columnspan=8, padx=20, pady=(0, 20), sticky="nsew")
        self.video_feed.insert("0.0", "VIDEO_OFFLINE")

        # options tabs

        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=1, column=2, padx=20, pady=20)

        # window buttons

        x_window_group: int = 8
        y_window_group: int = 0

        self.button = customtkinter.CTkButton(master=self, command=self.max_window, text="Maximize")
        self.button.grid(row=y_window_group, column=x_window_group, padx=200, pady=20, sticky="w")

        self.button = customtkinter.CTkButton(master=self, command=self.mini_window, text="Minimize")
        self.button.grid(row=y_window_group, column=x_window_group, padx=(190, 0), pady=20, sticky=None)

        self.button = customtkinter.CTkButton(master=self, command=self.close_window, text="Close")
        self.button.grid(row=y_window_group, column=x_window_group, padx=10, pady=20, sticky="e")

        # movement buttons

        x_movement_group: int = 2
        y_movement_group: int = 4

        self.button = customtkinter.CTkButton(master=self, command=self.button_callback, text="Forw.")
        self.button.grid(row=y_movement_group, column=x_movement_group, padx=10, pady=30, sticky='n')

        self.button = customtkinter.CTkButton(master=self, command=self.button_callback, text="Right")
        self.button.grid(row=y_movement_group, column=x_movement_group, padx=0, pady=30, sticky='e')

        self.button = customtkinter.CTkButton(master=self, command=self.button_callback, text="Back")
        self.button.grid(row=y_movement_group, column=x_movement_group, padx=10, pady=30, sticky='s')

        self.button = customtkinter.CTkButton(master=self, command=self.button_callback, text="Left")
        self.button.grid(row=y_movement_group, column=x_movement_group, padx=0, pady=30, sticky='w')

        # gripper buttons

        x_gripper_group: int = 2
        y_gripper_group: int = 4

        self.button = customtkinter.CTkButton(master=self, command=None, text="Claw Open")
        self.button.grid(row=y_gripper_group, column=x_gripper_group, padx=(10, 0), pady=40, sticky="ne")
        
        self.button = customtkinter.CTkButton(master=self, command=None, text="Claw Close")
        self.button.grid(row=y_gripper_group, column=x_gripper_group, padx=(0, 10), pady=40, sticky="nw")

        self.button = customtkinter.CTkButton(master=self, command=None, text="Claw Right")
        self.button.grid(row=y_gripper_group, column=x_gripper_group, padx=(10, 0), pady=40, sticky="se")
        
        self.button = customtkinter.CTkButton(master=self, command=None, text="Claw Left")
        self.button.grid(row=y_gripper_group, column=x_gripper_group, padx=(0, 10), pady=40, sticky="sw")

        # arm buttons

        x_arm_group: int = 2
        y_arm_group: int = 4

        self.button = customtkinter.CTkButton(master=self, command=None, text="Extend Arm")
        self.button.grid(row=y_arm_group, column=x_arm_group, padx=20, pady=0, sticky="n")

        self.button = customtkinter.CTkButton(master=self, command=None, text="Retract Arm")
        self.button.grid(row=y_arm_group, column=x_arm_group, padx=20, pady=0, sticky="s")

        self.time_start()

        # main window
        self.vid = MyVideoCapture(0)

        self.canvas = tk.Canvas(self, width= self.vid.width, height= self.vid.height)
        self.canvas.grid(row=1, column=3, rowspan=8, columnspan=8, padx=20, pady=(0, 20), sticky="nsew")

        self.update()      
    
    def update(self):
        ret, frame = self.vid.get_frame()        
        if ret:
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
                self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)  
        self.after(15, self.update)

    def time_start(self):
        current_time: str = datetime.now().strftime("%H:%M:%S")
        self.time.delete("0.0", "end")
        self.time.insert("0.0", current_time)
        self.after(1000, self.time_start)

    def button_callback(self):
        print(self.state())

    def max_window(self):
        self.wm_attributes("-fullscreen", "True")

    def mini_window(self):
        self.wm_attributes("-fullscreen", "False")
    
    def close_window(self):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.attributes("-fullscreen", "True")
    app.mainloop()