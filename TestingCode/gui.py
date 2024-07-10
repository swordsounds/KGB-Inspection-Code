import cv2
import customtkinter
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
import socket
import pickle

class ClientVideoCapture:
    '''
    Edit code below
    '''
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host_ip = '127.0.0.1'
    port = 6666
    socket_address = (host_ip, port)
    server.bind(socket_address)

    def get_frame(self, data):
        frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
        # dim = (1100, 720)
        # resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

class MyVideoCapture:

    res_width, res_height = (2048, 1536) #highest on pi is 1920, 1080

    def __init__(self, video_source: int) -> None:
        self.vid = cv2.VideoCapture(video_source)
        self.rec = None
        self.width = self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, self.res_width)
        self.height = self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, self.res_height)
        self.fps = self.vid.set(cv2.CAP_PROP_FPS, 30.0) #must use 10.0 on pi
        self.expo = self.vid.set(cv2.CAP_PROP_EXPOSURE, -4.0) #set to -60/0 for pi

    def get_frame(self) -> tuple[bool, list[int]]:
        ret, frame = self.vid.read()
        if rec_toggle:
                self.rec.write(frame)
        dim = (1100, 720)
        resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        return (ret, cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
    
    def get_rec(self) -> object:
        file_name = f"video{rec_counter}.avi"
        fourcc = cv2.VideoWriter_fourcc(*'FMP4')
        fps = 5.0
        res = (self.res_width, self.res_height)
        self.rec = cv2.VideoWriter(file_name, fourcc, fps, res)
        return self.rec

    def get_pic(self) -> None:
        ret, frame = self.vid.read()
        if ret:
            img_name = f'opencv_frame_{img_counter}'
            cv2.imwrite(f"{img_name}.png", frame)
    
    def __del__(self) -> None:
        if self.vid.isOpened():
            try:
                self.vid.release()
                self.rec.release()
            except Exception as e:
                print(e)

class TetherButtonGroup(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.extend = 0 # test code REMOVE

        # tether buttons
        self.grid_rowconfigure(tuple(range(9)), weight=1)
        self.grid_columnconfigure(tuple(range(9)), weight=1)

        self.label = customtkinter.CTkLabel(self, text="Tether")
        self.label.grid(row=0, column=0, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.tether_extend, text="Extend Tether")
        self.button.grid(row=1, column=0, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.tether_stop, text="Stop Tether")
        self.button.grid(row=1, column=1, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.tether_retract, text="Retract Tether")
        self.button.grid(row=1, column=2, padx=20, pady=20)

    def tether_extend(self):
        print("extending tether")
        # client.print_message(self.extend) # test code REMOVE
        
    
    def tether_stop(self):
        print("tether stopped")
    
    def tether_retract(self):
        print("retracting tether")

class MovementButtonGroup(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # movement buttons

        self.grid_rowconfigure(tuple(range(9)), weight=1)
        self.grid_columnconfigure(tuple(range(9)), weight=1)

        self.label = customtkinter.CTkLabel(self, text="Movement")
        self.label.grid(row=0, column=0, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.crawler_forward, text="Forw.")
        self.button.grid(row=1, column=0, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.crawler_right, text="Right")
        self.button.grid(row=1, column=1, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.crawler_backward, text="Back")
        self.button.grid(row=1, column=2, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.crawler_left, text="Left")
        self.button.grid(row=1, column=3, padx=20, pady=20)

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
        self.label.grid(row=0, column=0, pady=20)

        # gripper buttons

        self.button = customtkinter.CTkButton(master=self, command=self.gripper_open, text="Claw Open")
        self.button.grid(row=1, column=0, padx=20, pady=20)
        
        self.button = customtkinter.CTkButton(master=self, command=self.gripper_close, text="Claw Close")
        self.button.grid(row=1, column=1, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.gripper_right, text="Claw Right")
        self.button.grid(row=1, column=2, padx=20, pady=20)
        
        self.button = customtkinter.CTkButton(master=self, command=self.gripper_left, text="Claw Left")
        self.button.grid(row=1, column=3, padx=20, pady=20)

    def gripper_open(self):
        print("gripper opened")

    def gripper_close(self):
        print("gripper closed")

    def gripper_left(self):
        print("gripper wrist left")
        
    def gripper_right(self):
        print("gripper wrist right")

class ArmButtonGroup(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = customtkinter.CTkLabel(self, text="Arm")
        self.label.grid(row=0, column=0, pady=20)

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
        self.geometry("{}x{}".format(width, height))

        self.title("Control Panel")
        self.wm_iconbitmap(default=None)
        self.minsize(300, 200)

        
        '''
        Background code, gotta fix buttons corner radius
        '''
        # background_image = customtkinter.CTkImage(Image.open("carbon-fiber-manufacturing-848x500.jpg"), size=(width, height))
        # bg_lbl = customtkinter.CTkLabel(self, text="", image=background_image)
        # bg_lbl.place(x=0, y=-1)

        # 20x20 grid system

        self.grid_rowconfigure(tuple(range(21)), weight=1)
        self.grid_columnconfigure(tuple(range(21)), weight=1)

        # logo 

        # kgb_logo = customtkinter.CTkImage(Image.open("logo.jpg"), size=(250, 150))
        # logo = customtkinter.CTkLabel(self, text="", image=kgb_logo)
        # logo.grid(row=1, column=0, sticky="w")

        # time display 

        self.time = customtkinter.CTkTextbox(master=self,height=10, font=("", 20))
        self.time.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        self.time.insert("0.0", 'CURRENT_TIME')
        self.time_start()

        # window buttons

        self.button = customtkinter.CTkButton(master=self, command=self.max_window, text="Maximize")
        self.button.grid(row=0, column=18, padx=(200, 0), pady=20, sticky="e")

        self.button = customtkinter.CTkButton(master=self, command=self.mini_window, text="Minimize")
        self.button.grid(row=0, column=19, padx=(40, 0), pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.close_window, text="Close")
        self.button.grid(row=0, column=20, padx=(0, 20), pady=20, sticky="e")

        # tether buttons

        self.frame = TetherButtonGroup(master=self)
        self.frame.grid(row=2, column=0, columnspan=1, padx=(20, 0), pady=20, sticky="ew")

        # movement frame

        self.frame = MovementButtonGroup(master=self)
        self.frame.grid(row=3, column=0, columnspan=2, padx=(20, 0), pady=20, sticky="ew")

        # gripper frame

        self.frame = GripperButtonGroup(master=self)
        self.frame.grid(row=4, column=0, columnspan=2, padx=(20, 0), pady=20, sticky="ew")

        # arm frame

        self.frame = ArmButtonGroup(master=self)
        self.frame.grid(row=5, column=0, padx=(20, 0), pady=20, sticky="w")
        
       # video buttons
        self.label = customtkinter.CTkLabel(self, text="Video Settings")
        self.label.grid(row=1, column=1, padx=20, pady=(50, 0), sticky="se")

        self.record_on = customtkinter.CTkButton(master=self, command=self.program_take_recording, text="Rec.")
        self.record_on.grid(row=2, column=1, padx=0, pady=(0,50), sticky="ne")

        self.record_off = customtkinter.CTkButton(master=self, command=self.program_stop_recording, text="Stop Rec.")
        self.record_off.grid(row=2, column=1, padx=0, pady=0, sticky="e")

        self.button = customtkinter.CTkButton(master=self, command=self.program_take_picture, text="Take Pic.")
        self.button.grid(row=2, column=1, padx=0, pady=(50, 0), sticky="se")

        # test code FIX

        self.server = ClientVideoCapture()
        self.video_frame = tk.Canvas(self, width='640', height='480')
        self.video_frame.grid(row=1, column=2, rowspan=4, columnspan=20,padx=20, pady=20,sticky="nsew")
        self.server_update()
        # video device 

    #     self.vid = MyVideoCapture(0)
    #     self.canvas = tk.Canvas(self, width=self.vid.width, height=self.vid.height)
    #     self.canvas.grid(row=1, column=2, rowspan=4, columnspan=20,padx=20, pady=20,sticky="nsew")
    #     self.video_update()      

    # def video_update(self):
    #     try:
    #         ret, frame = self.vid.get_frame()        
    #         if ret:
    #                 self.photo = ImageTk.PhotoImage(image= Image.fromarray(frame))
    #                 self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)  
    #         self.after(15, self.video_update)
    #     except Exception as e:
    #         print(e)

    def server_update(self):
        bytes: list[str, tuple[str, int]] = server.recvfrom(1000000)
        data = pickle.loads(bytes[0])

        frame = self.server.get_frame(data)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame)) 
        self.video_frame.create_image(0, 0, image=self.photo, anchor=tk.NW)  
        self.after(15, self.server_update)

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
        # del self.vid
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.wm_attributes('-fullscreen', True)
    app.state('normal')
    app.mainloop()