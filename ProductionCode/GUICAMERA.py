import cv2, tkinter as tk, customtkinter # type: ignore
from PIL import Image, ImageTk # type: ignore
import uuid

import multiprocessing
import socket, pickle

from config import *

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2048)

def server_listener_start(info_to_control):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2048)
    server.bind((SERVER_CONTROL_BOX, CTRLBXPORT_1))
    temp = {}
    try:
        while True:
            data_from_crawler = server.recvfrom(2048)
            data_from_crawler = data_from_crawler[0]
            data = pickle.loads(data_from_crawler) 
            for key, value in data.items():
                temp[key] = value
            info_to_control.value = temp
    except Exception as e:
        print(e)

class VideoCaptureDevice:
    #highest res on pi is 1280, 720 using usb
    

    def __init__(self, video_link):
        self.vid = cv2.VideoCapture(video_link) #change ip in prod 192.168.0.19
        self.rec = None

    def get_frame(self) -> tuple[bool, list[int]]:
        ret, frame = self.vid.read()
        if rec_toggle:
                self.rec.write(frame)
        resized = cv2.resize(frame, (960, 540), interpolation=cv2.INTER_AREA)
        return (ret, cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
    
    def get_rec(self) -> object:
        unique_id = str(uuid.uuid4()).split('-')[0] #test code TEST THIS
        file_name = f"{unique_id}.avi"
        fourcc = cv2.VideoWriter_fourcc(*'FMP4')#*'FMP4'
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

class CameraButtonGroup(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = customtkinter.CTkLabel(self, text="ARDUCAM Settings")
        self.label.grid(row=0, column=0, pady=20)

        # 8x8 grid
        self.grid_rowconfigure(tuple(range(9)), weight=1)
        self.grid_columnconfigure(tuple(range(9)), weight=1)
        
        # Camera selector buttons

        self.button = customtkinter.CTkButton(master=self, command=self.cam_one, text="Channel 1")
        self.button.grid(row=1, column=0, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.cam_two, text="Channel 2")
        self.button.grid(row=1, column=1, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.cam_three, text="Channel 3")
        self.button.grid(row=2, column=0, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.cam_four, text="Channel 4")
        self.button.grid(row=2, column=1, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.reset, text="Reset")
        self.button.grid(row=1, column=2,padx=20, pady=20)

    def cam_one(self):
        info_to_crawler = {'ARDU_CAMERA': 'ONE'}
        x_as_bytes = pickle.dumps(info_to_crawler)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))

    def cam_two(self):
        info_to_crawler = {'ARDU_CAMERA': 'TWO'}
        x_as_bytes = pickle.dumps(info_to_crawler)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))

    def cam_three(self):
        info_to_crawler = {'ARDU_CAMERA': 'THREE'}
        x_as_bytes = pickle.dumps(info_to_crawler)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))

    def cam_four(self):
        info_to_crawler = {'ARDU_CAMERA': 'FOUR'}
        x_as_bytes = pickle.dumps(info_to_crawler)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))

    def reset(self):
        info_to_crawler = {'ARDU_CAMERA': 'RESET'}
        x_as_bytes = pickle.dumps(info_to_crawler)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))

class PTZButtonGroup(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = customtkinter.CTkLabel(self, text="PTZ Settings")
        self.label.grid(row=0, column=0, pady=20)
        
        # 8x8 grid
        self.grid_rowconfigure(tuple(range(9)), weight=1)
        self.grid_columnconfigure(tuple(range(9)), weight=1)

        # PTZ buttons

        self.button = customtkinter.CTkButton(master=self, command=self.servo_up, text="Up")
        self.button.grid(row=1, column=0, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.servo_right, text="Right")
        self.button.grid(row=1, column=1, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.servo_down, text="Down")
        self.button.grid(row=1, column=2, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.servo_left, text="Left")
        self.button.grid(row=1, column=3, padx=20, pady=20)

        # focus buttons

        self.focus = customtkinter.CTkSlider(master=self, from_=0, to=20000, command=self.focus_slider)
        self.focus.set(0)
        self.focus.grid(row=2, column=3, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.more_focus, text="Focus In")
        self.button.grid(row=2, column=0, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.less_focus, text="Focus Out")
        self.button.grid(row=2, column=1, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.auto_focus, text="Auto Focus")
        self.button.grid(row=2, column=2, padx=20, pady=20)

        # zoom buttons

        self.zoom = customtkinter.CTkSlider(master=self, from_=0, to=20000, command=self.zoom_slider)
        self.zoom.set(3000)
        self.zoom.grid(row=3, column=3, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.more_zoom, text="Zoom In")
        self.button.grid(row=3, column=0, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.less_zoom, text="Zoom Out")
        self.button.grid(row=3, column=1, padx=20, pady=20)

        # ir cut

        self.button = customtkinter.CTkButton(master=self, command=self.ir_cut, text="IR Cut")
        self.button.grid(row=3, column=2, padx=20, pady=20)

        # zoom and focus change

        self.zoom_and_focus_change()

    def zoom_slider(self, value):
        info_to_crawler = {'PTZ_ZOOM': f'ON_{round(value)}'}
        x_as_bytes = pickle.dumps(info_to_crawler)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))
    
    def focus_slider(self, value):
        info_to_crawler = {'PTZ_FOCUS': f'ON_{round(value)}'}
        x_as_bytes = pickle.dumps(info_to_crawler)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))

    def more_zoom(self):
        info_to_crawler = {'PTZ_ZOOM': '+'}
        x_as_bytes = pickle.dumps(info_to_crawler)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))

    def less_zoom(self):
        info_to_crawler = {'PTZ_ZOOM': '-'}
        x_as_bytes = pickle.dumps(info_to_crawler)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))

    def more_focus(self):
        info_to_crawler = {'PTZ_FOCUS': '+'}
        x_as_bytes = pickle.dumps(info_to_crawler)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))

    def less_focus(self):
        info_to_crawler = {'PTZ_FOCUS': '-'}
        x_as_bytes = pickle.dumps(info_to_crawler)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))
        
    def auto_focus(self):
        info_to_crawler = {'PTZ_FOCUS': 'AUTO'}
        x_as_bytes = pickle.dumps(info_to_crawler)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))

    def servo_left(self):
        info = {'PTZ_MOVEMENT': 'LEFT'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))

    def servo_right(self):
        info_to_crawler = {'PTZ_MOVEMENT': 'RIGHT'}
        x_as_bytes = pickle.dumps(info_to_crawler)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))
    
    def servo_up(self):
        info_to_crawler = {'PTZ_MOVEMENT': 'UP'}
        x_as_bytes = pickle.dumps(info_to_crawler)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))

    def servo_down(self):
        info_to_crawler = {'PTZ_MOVEMENT': 'DOWN'}
        x_as_bytes = pickle.dumps(info_to_crawler)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))
    
    def ir_cut(self):
        info_to_crawler = {'IR_CUT': 'True'}
        x_as_bytes = pickle.dumps(info_to_crawler)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))

    def zoom_and_focus_change(self):
        self.focus.set(int(info_to_control.value['FOCUS']))
        self.zoom.set(int(info_to_control.value['ZOOM']))
        self.after(3000, self.zoom_and_focus_change)

class App(customtkinter.CTk):

    customtkinter.set_appearance_mode("dark")
    global rec_toggle, video_screen_dim
    rec_toggle = False
    video_screen_dim = (1280, 720)
   
    def __init__(self):
        super().__init__()

        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        # self.geometry("{}x{}-{}+0".format(width, height, width + 8)) # added 8 pixels translation due to weird scaling :/
        self.geometry("{}x{}+0+0".format(width, height)) # added 8 pixels translation due to weird scaling :/
        self.title("Video Panel")
        self.wm_iconbitmap(default=None)
        self.maxsize(width=1920, height=height)
        

        # logo 

        kgb_logo = customtkinter.CTkImage(Image.open("KGB_Logo.png"), size=(160, 75))
        logo = customtkinter.CTkLabel(self, text="", image=kgb_logo)
        logo.grid(row=5, column=9, sticky="ne")

        # 9  x9 grid system

        self.grid_rowconfigure(tuple(range(10)), weight=1)
        self.grid_columnconfigure(tuple(range(10)), weight=1)
        
        # Camera buttons

        self.frame = CameraButtonGroup(master=self)
        self.frame.grid(row=2, column=0, columnspan=1 ,padx=(20, 20), pady=20, sticky='w')

        # PTZ buttons

        self.frame = PTZButtonGroup(master=self)
        self.frame.grid(row=3, column=0, rowspan=1, columnspan=1, padx=(20, 20), pady=20, sticky='ew')
    
        # window buttons

        self.button = customtkinter.CTkButton(master=self, command=self.max_window, text="Maximize")
        self.button.grid(row=0, column=7, padx=(200, 0), pady=20, sticky="e")

        self.button = customtkinter.CTkButton(master=self, command=self.mini_window, text="Minimize")
        self.button.grid(row=0, column=8, padx=(40, 0), pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.close_window, text="Close")
        self.button.grid(row=0, column=9, padx=(0, 20), pady=20, sticky="e")
        
        # video buttons
        self.label = customtkinter.CTkLabel(self, text="Video Settings")
        self.label.grid(row=2, column=0, padx=20, pady=(0, 0), sticky="ne")

        self.record_on = customtkinter.CTkButton(master=self, command=self.program_take_recording, text="Rec.")
        self.record_on.grid(row=2, column=0, padx=0, pady=(50,50), ipadx=10, sticky="ne")

        self.record_off = customtkinter.CTkButton(master=self, command=self.program_stop_recording, text="Stop Rec.")
        self.record_off.grid(row=2, column=0, padx=0, pady=(100,0), ipadx=10, sticky="ne")

        self.button = customtkinter.CTkButton(master=self, command=self.program_take_picture, text="Take Pic.")
        self.button.grid(row=2, column=0, padx=0, pady=(150, 0), ipadx=10, sticky="ne")

        # camera selector 
        self.combobox = customtkinter.CTkComboBox(master=self, values=["ARDUCam.", "PTZ Cam.", "Rear Cam."],
                                            command=self.combobox_callback)
        self.combobox.set('Select Camera')
        self.combobox.grid(row=2, column=0, pady=(200, 0), ipadx=10,sticky="ne")

        # video device 
        self.vid = VideoCaptureDevice('http://192.168.0.19:9000/stream.mjpg')
        self.canvas = tk.Canvas(self, width=1080, height=0, bg='#242424', highlightthickness=0) #adjusted height by -95px to remove whitespace :/
        self.canvas.grid(row=1, column=1, rowspan=3, columnspan=9,padx=20, pady=20,sticky="nsew")
        self.video_update()

        # info resetter

        self.info_reset()

    def combobox_callback(self, choice):
        if choice == 'PTZ Cam.':
            self.vid = VideoCaptureDevice('http://192.168.0.19:9100/stream.mjpg') 

        elif choice == 'ARDUCam.':
            self.vid = VideoCaptureDevice('http://192.168.0.19:9000/stream.mjpg')
            
        elif choice == 'Rear Cam.':
            self.vid = VideoCaptureDevice('http://192.168.0.19:9300/stream.mjpg')

    def video_update(self):
        try:
            ret, frame = self.vid.get_frame()        
            if ret:
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(100, 0, image=self.photo, anchor=tk.NW)  
            self.after(15, self.video_update)
        except Exception as e:
            print(e)

    def program_take_recording(self):
        global rec_toggle
        self.record_on.configure(state='disabled')
        self.vid.get_rec()
        rec_toggle = True

    def program_stop_recording(self):
        global rec_toggle
        self.record_on.configure(state='enabled')
        rec_toggle = False
    
    def program_take_picture(self):
        self.vid.get_pic()

    def max_window(self):
        self.geometry("{}x{}-{}+0".format(1920, 1080, 1928))
        
    def mini_window(self):
        self.geometry("{}x{}-{}+0".format(300, 300, 1925))
    
    def close_window(self):
        self.destroy()

    def info_reset(self):
        info_to_crawler = {'PTZ_ZOOM': '', 'PTZ_FOCUS': '', 'PTZ_MOVEMENT': '', 'IR_CUT': ''}
        x_as_bytes = pickle.dumps(info_to_crawler)
        server.sendto((x_as_bytes), (SERVER_CRAWLER, CMDPORT))
        self.after(50, self.info_reset)

if __name__ == "__main__":
    info_to_control = multiprocessing.Manager().Value('i', {'FOCUS': 0, 'ZOOM': 0})
    t = multiprocessing.Process(target=server_listener_start, args=(info_to_control,))
    app = App()
    t.start()
    app.mainloop()