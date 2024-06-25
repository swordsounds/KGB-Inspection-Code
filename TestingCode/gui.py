import cv2
import customtkinter
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime

class MyVideoCapture:
    def __init__(self, video_source: int) -> None:
        self.vid = cv2.VideoCapture(video_source)
        self.rec = None
        self.width = self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.height = self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.expo = self.vid.set(cv2.CAP_PROP_EXPOSURE, -3.0)

    def get_frame(self) -> tuple[bool, list[int]]:
        ret, frame = self.vid.read()
        if rec_toggle:
                self.rec.write(frame)
        dim = (1200, 1000)
        resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        return (ret, cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
    
    def get_rec(self):
        file_name = f"video{rec_counter}.avi"
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = 30.0
        res = (1920, 1080)
        self.rec = cv2.VideoWriter(file_name, fourcc, fps, res)
        return self.rec

    def get_pic(self):
        ret, frame = self.vid.read()
        if ret:
            img_name = f'opencv_frame_{img_counter}'
            cv2.imwrite(f"{img_name}.png", frame)
    
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

class MovementButtonGroup(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # movement buttons

        self.grid_rowconfigure(tuple(range(9)), weight=1)
        self.grid_columnconfigure(tuple(range(9)), weight=1)

        self.label = customtkinter.CTkLabel(self, text="Movement")
        self.label.grid(row=0, column=0, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.crawler_forward, text="Forw.")
        self.button.grid(row=1, column=0, padx=20, pady=20, sticky="ns")

        self.button = customtkinter.CTkButton(master=self, command=self.crawler_right, text="Right")
        self.button.grid(row=1, column=1, padx=20, pady=20, sticky="e")

        self.button = customtkinter.CTkButton(master=self, command=self.crawler_backward, text="Back")
        self.button.grid(row=1, column=2, padx=20, pady=20, sticky="s")

        self.button = customtkinter.CTkButton(master=self, command=self.crawler_left, text="Left")
        self.button.grid(row=1, column=3, padx=20, pady=20, sticky="w")

    def crawler_forward(self):
        print("Crawler forward")

    def crawler_right(self):
        print("Crawler right")

    def crawler_backward(self):
        print("Crawler backwards")

    def crawler_left(self):
        print("Crawler left")

class GripperButtonGroup(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = customtkinter.CTkLabel(self, text="Claw")
        self.label.grid(row=0, column=0, padx=20)

        # gripper buttons

        x_gripper_group: int = 2
        y_gripper_group: int = 4

        self.button = customtkinter.CTkButton(master=self, command=self.gripper_open, text="Claw Open")
        self.button.grid(row=1, column=0, padx=20, pady=40)
        
        self.button = customtkinter.CTkButton(master=self, command=self.gripper_close, text="Claw Close")
        self.button.grid(row=1, column=1, padx=20, pady=40)

        self.button = customtkinter.CTkButton(master=self, command=self.gripper_right, text="Claw Right")
        self.button.grid(row=1, column=2, padx=20, pady=40)
        
        self.button = customtkinter.CTkButton(master=self, command=self.gripper_left, text="Claw Left")
        self.button.grid(row=1, column=3, padx=20, pady=40)

    def gripper_open(self):
        print("gripper opened")

    def gripper_close(self):
        print("gripper closed")

    def gripper_left(self):
        print("gripper wrist left")
        
    def gripper_right(self):
        print("gripper wrist right")

class ArmButtonGroup(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = customtkinter.CTkLabel(self, text="Arm")
        self.label.grid(row=0, column=0, padx=20)

        # arm buttons

        self.button = customtkinter.CTkButton(master=self, command=self.arm_extend, text="Extend Arm")
        self.button.grid(row=1, column=0, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.arm_retract, text="Retract Arm")
        self.button.grid(row=1, column=1, padx=20, pady=20)

    def arm_extend(self):
        print("arm extended")

    def arm_retract(self):
        print("arm retracted")


class App(customtkinter.CTk):

    customtkinter.set_appearance_mode("dark")
    global rec_toggle, img_counter, rec_counter
    rec_toggle = False
    rec_counter = 0
    img_counter = 0

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

        self.grid_rowconfigure(tuple(range(21)), weight=1)
        self.grid_columnconfigure(tuple(range(21)), weight=1)

        # time display 

        self.time = customtkinter.CTkTextbox(master=self,height=10, font=("", 20))
        self.time.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        self.time.insert("0.0", 'CURRENT_TIME')
        self.time_start()

        # options tabs

        # self.tab_view = MyTabView(master=self)
        # self.tab_view.grid(row=1, column=2, padx=20, pady=20)

        # window buttons

        self.button = customtkinter.CTkButton(master=self, command=self.max_window, text="Maximize")
        self.button.grid(row=0, column=18, padx=(200, 0), pady=20, sticky="e")

        self.button = customtkinter.CTkButton(master=self, command=self.mini_window, text="Minimize")
        self.button.grid(row=0, column=19, padx=(40, 0), pady=20, sticky=None)

        self.button = customtkinter.CTkButton(master=self, command=self.close_window, text="Close")
        self.button.grid(row=0, column=20, padx=(0, 20), pady=20, sticky="e")
        
        # movement frame

        self.frame = MovementButtonGroup(master=self)
        self.frame.grid(row=3, column=0, columnspan=2, padx=(20, 0), pady=20, sticky="w")

        # gripper frame

        self.frame = GripperButtonGroup(master=self)
        self.frame.grid(row=4, column=0, columnspan=2, padx=(20, 0), pady=20, sticky="w")

        # arm frame

        self.frame = ArmButtonGroup(master=self)
        self.frame.grid(row=2, column=0, columnspan=3, padx=(20, 0), pady=20, sticky="w")
        
     

       # video buttons
        self.label = customtkinter.CTkLabel(self, text="Video Settings")
        self.label.grid(row=1, column=1, padx=20, pady=(50, 0), sticky="se")

        self.button = customtkinter.CTkButton(master=self, command=self.program_take_recording, text="Rec.")
        self.button.grid(row=2, column=1, padx=0, pady=(0,50), sticky="ne")

        self.button = customtkinter.CTkButton(master=self, command=self.program_stop_recording, text="Stop Rec.")
        self.button.grid(row=2, column=1, padx=0, pady=0, sticky="e")

        self.button = customtkinter.CTkButton(master=self, command=self.program_take_picture, text="Take Pic.")
        self.button.grid(row=2, column=1, padx=0, pady=(50, 0), sticky="se")

        # video device 

        self.vid = MyVideoCapture(1)

        self.canvas = tk.Canvas(self, width=self.vid.width, height=self.vid.height)
        self.canvas.grid(row=1, column=2, rowspan=20, columnspan=20,padx=20, pady=20,sticky="nsew")
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

    def program_take_recording(self):
        global rec_toggle, rec_counter
        self.vid.get_rec()
        rec_counter += 1
        rec_toggle = True

    def program_stop_recording(self):
        global rec_toggle
        rec_toggle = False
    
    def program_take_picture(self):
        global img_counter
        img_counter += 1
        self.vid.get_pic()

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

   
    
    def tether_extend(self):
        print("extending tether")
    
    def tether_stop(self):
        print("tether stopped")
    
    def tether_retract(self):
        print("retracting tether")
    
if __name__ == "__main__":
    app = App()
    app.attributes("-fullscreen", "True")
    app.mainloop()