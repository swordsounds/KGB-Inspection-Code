import cv2, tkinter as tk, customtkinter
from PIL import Image, ImageTk
from datetime import datetime
import uuid, socket, pickle

SERVER = '127.0.0.1'
CMDPORT = 8000 

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2048)

class VideoCaptureDevice:
    #highest res on pi is 1280, 720
    def __init__(self):
        self.vid = cv2.VideoCapture('http://192.168.0.19:9000/') #change ip in prod 192.168.0.19
        self.rec = None

    def get_frame(self) -> tuple[bool, list[int]]:
        ret, frame = self.vid.read()
        if rec_toggle:
                self.rec.write(frame)
        resized = cv2.resize(frame, video_screen_dim, interpolation=cv2.INTER_AREA)
        return (ret, cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
    
    def get_rec(self) -> object:
        unique_id = str(uuid.uuid4()).split('-')[0] #test code TEST THIS
        file_name = f"{unique_id}.avi"
        fourcc = cv2.VideoWriter_fourcc(*'XVID')#*'FMP4'
        fps = 10.0
        res = (1280, 720)
        self.rec = cv2.VideoWriter(file_name, fourcc, fps, res)
        return self.rec

    def get_pic(self) -> None:
        ret, frame = self.vid.read()
        if ret:
            unique_id = str(uuid.uuid4()).split('-')[0] #test code TEST THIS
            cv2.imwrite(f"{unique_id}.png", frame)
    
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

    @staticmethod
    def tether_extend():  
        info = {'tether': 'extend'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    @staticmethod       
    def tether_stop():
        info = {'tether': 'stop'}

        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    @staticmethod    
    def tether_retract():
        info = {'tether': 'retract'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

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

    @staticmethod
    def crawler_forward():
        info = {'crawl': 'forward'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    @staticmethod
    def crawler_backward():
        info = {'crawl': 'backward'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    @staticmethod
    def crawler_right():
        info = {'crawl': 'right'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    @staticmethod
    def crawler_left():
        info = {'crawl': 'left'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

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

    @staticmethod
    def gripper_open():
        info = {'gripper': 'open'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    @staticmethod
    def gripper_close():
        info = {'gripper': 'closed'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    @staticmethod
    def gripper_left():
        info = {'gripper': 'left'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    @staticmethod       
    def gripper_right():
        info = {'gripper': 'right'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

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

    @staticmethod
    def arm_extend():
        info = {'arm': 'extend'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))
        
    @staticmethod      
    def arm_retract():
        info = {'arm': 'retract'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))
      

class App(customtkinter.CTk):

    customtkinter.set_appearance_mode("dark")
    global rec_toggle, video_screen_dim
    rec_toggle = False
    video_screen_dim = (1280, 720)

    def __init__(self):
        super().__init__()

        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("{}x{}".format(width, height))
        self.title("Control Panel")
        self.wm_attributes('-fullscreen', True)
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

        kgb_logo = customtkinter.CTkImage(Image.open("Assets\logo.jpg"), size=(125, 75))
        logo = customtkinter.CTkLabel(self, text="", image=kgb_logo)
        logo.grid(row=0, column=0, sticky="n")

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

        # video device 

        self.vid = VideoCaptureDevice()
        self.canvas = tk.Canvas(self, width=1280, height=700) #adjusted height by -20px to remove whitespace :/
        self.canvas.grid(row=1, column=2, rowspan=4, columnspan=20,padx=20, pady=20,sticky="nsew")
        self.video_update()      
        
    def video_update(self):
        try:
            ret, frame = self.vid.get_frame()        
            if ret:
                    self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                    self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)  
            self.after(15, self.video_update)
        except Exception as e:
            print(e)

    def program_take_recording(self):
        global rec_toggle
        self.vid.get_rec()
        rec_toggle = True

    def program_stop_recording(self):
        global rec_toggle
        rec_toggle = False
    
    def program_take_picture(self):
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
   
if __name__ == "__main__":
    app = App()
    app.mainloop()