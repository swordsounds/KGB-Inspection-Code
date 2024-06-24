import cv2
import customtkinter
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime

class MyVideoCapture:
    def __init__(self, video_source: int) -> None:
        self.vid = cv2.VideoCapture(video_source)
        self.rec = cv2.VideoWriter("video.avi", cv2.VideoWriter_fourcc(*'XVID'), 30.0, (1920, 1080))
        self.width = self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.height = self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    def get_frame(self) -> tuple[bool, list[int]]:
        ret, frame = self.vid.read()
        dim = (1200, 1000)
        resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        self.rec.write(frame)
        return (ret, cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
    
    def __del__(self):
        if self.vid.isOpened():
            self.rec.release()
            self.vid.release()

class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master):
        super().__init__(master)

        # self.add("Video/Pic")
        self.add("Tether")

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
        self.time_start()

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

        self.button = customtkinter.CTkButton(master=self, command=self.crawler_forward, text="Forw.")
        self.button.grid(row=y_movement_group, column=x_movement_group, padx=10, pady=30, sticky='n')

        self.button = customtkinter.CTkButton(master=self, command=self.crawler_right, text="Right")
        self.button.grid(row=y_movement_group, column=x_movement_group, padx=0, pady=30, sticky='e')

        self.button = customtkinter.CTkButton(master=self, command=self.crawler_backward, text="Back")
        self.button.grid(row=y_movement_group, column=x_movement_group, padx=10, pady=30, sticky='s')

        self.button = customtkinter.CTkButton(master=self, command=self.crawler_left, text="Left")
        self.button.grid(row=y_movement_group, column=x_movement_group, padx=0, pady=30, sticky='w')

        # gripper buttons

        x_gripper_group: int = 2
        y_gripper_group: int = 4

        self.button = customtkinter.CTkButton(master=self, command=self.gripper_open, text="Claw Open")
        self.button.grid(row=y_gripper_group, column=x_gripper_group, padx=(10, 0), pady=40, sticky="ne")
        
        self.button = customtkinter.CTkButton(master=self, command=self.gripper_close, text="Claw Close")
        self.button.grid(row=y_gripper_group, column=x_gripper_group, padx=(0, 10), pady=40, sticky="nw")

        self.button = customtkinter.CTkButton(master=self, command=self.gripper_right, text="Claw Right")
        self.button.grid(row=y_gripper_group, column=x_gripper_group, padx=(10, 0), pady=40, sticky="se")
        
        self.button = customtkinter.CTkButton(master=self, command=self.gripper_left, text="Claw Left")
        self.button.grid(row=y_gripper_group, column=x_gripper_group, padx=(0, 10), pady=40, sticky="sw")

        # arm buttons

        x_arm_group: int = 2
        y_arm_group: int = 4

        self.button = customtkinter.CTkButton(master=self, command=self.arm_extend, text="Extend Arm")
        self.button.grid(row=y_arm_group, column=x_arm_group, padx=20, pady=0, sticky="n")

        self.button = customtkinter.CTkButton(master=self, command=self.arm_retract, text="Retract Arm")
        self.button.grid(row=y_arm_group, column=x_arm_group, padx=20, pady=0, sticky="s")
        
        # video buttons

        self.button = customtkinter.CTkButton(master=self, command=self.program_take_recording, text="Rec.")
        self.button.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.button = customtkinter.CTkButton(master=self, command=None, text="Stop Rec.")
        self.button.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.button = customtkinter.CTkButton(master=self, command=None, text="Take Pic.")
        self.button.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        # video device 

        self.vid = MyVideoCapture(0)

        self.canvas = tk.Canvas(self, width=self.vid.width, height=self.vid.height)
        self.canvas.grid(row=1, column=3, rowspan=8, columnspan=8, padx=20, pady=(0, 20), sticky="nsew")
        self.video_update()      

    def video_update(self):
        try:
            ret, frame = self.vid.get_frame()        
            if ret:
                    self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
                    self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)  
            self.after(15, self.video_update)
        except Exception as e:
            print(e)


    def time_start(self):
        current_time: str = datetime.now().strftime("%H:%M:%S")
        self.time.delete("0.0", "end")
        self.time.insert("0.0", current_time)
        self.after(1000, self.time_start)

    def max_window(self):
        self.wm_attributes("-fullscreen", "True")

    def mini_window(self):
        self.wm_attributes("-fullscreen", "False")
    
    def close_window(self):
        self.destroy()

    def program_take_recording(self):
        # ret, frame = self.vid.get_frame() 
        # self.rec.write(frame)
        return

    
    def program_stop_recording(self):
        self.rec.release()
    
    def program_take_picture(self):
        return
    
    def tether_extend(self):
        return
    
    def tether_stop(self):
        return
    
    def tether_retract(self):
        return
    
    def crawler_forward(self):
        print("Crawler forward")

    def crawler_right(self):
        print("Crawler right")

    def crawler_backward(self):
        print("Crawler backwards")

    def crawler_left(self):
        print("Crawler left")
    
    def gripper_open(self):
        print("gripper opened")

    def gripper_close(self):
        print("gripper closed")

    def gripper_left(self):
        print("gripper wrist left")
        
    def gripper_right(self):
        print("gripper wrist right")
    
    def arm_extend(self):
        print("arm extended")

    def arm_retract(self):
        print("arm retracted")

if __name__ == "__main__":
    app = App()
    app.attributes("-fullscreen", "True")
    app.mainloop()