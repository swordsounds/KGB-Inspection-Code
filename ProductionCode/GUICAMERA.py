import cv2, tkinter as tk, customtkinter # type: ignore
from PIL import Image, ImageTk # type: ignore
import uuid, time

import socket, pickle

SERVER = '192.168.0.19' #change ip to static ip in prod
CMDPORT = 8000 

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2048)

class VideoCaptureDevice:
    #highest res on pi is 1280, 720 using usb
    

    def __init__(self, video_link):
        self.vid = cv2.VideoCapture(video_link) #change ip in prod 192.168.0.19
        self.rec = None

    def get_frame(self) -> tuple[bool, list[int]]:
        ret, frame = self.vid.read()
        if rec_toggle:
                self.rec.write(frame)
        resized = cv2.resize(frame, (video_screen_dim[0] - 150, video_screen_dim[1]), interpolation=cv2.INTER_AREA)
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
        info = {'ARDU_CAMERA': 'ONE'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    def cam_two(self):
        info = {'ARDU_CAMERA': 'TWO'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    def cam_three(self):
        info = {'ARDU_CAMERA': 'THREE'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    def cam_four(self):
        info = {'ARDU_CAMERA': 'FOUR'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    def reset(self):
        info = {'ARDU_CAMERA': 'RESET'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

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

        self.slider = customtkinter.CTkSlider(master=self, from_=0, to=100, command=self.focus_slider)
        self.slider.set(0)
        self.slider.grid(row=2, column=3, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.more_focus, text="Focus In")
        self.button.grid(row=2, column=0, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.less_focus, text="Focus Out")
        self.button.grid(row=2, column=1, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.auto_focus, text="Auto Focus")
        self.button.grid(row=2, column=2, padx=20, pady=20)

        # zoom buttons

        self.slider = customtkinter.CTkSlider(master=self, from_=0, to=100, command=self.zoom_slider)
        self.slider.set(0)
        self.slider.grid(row=3, column=3, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.more_zoom, text="Zoom In")
        self.button.grid(row=3, column=0, padx=20, pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.less_zoom, text="Zoom Out")
        self.button.grid(row=3, column=1, padx=20, pady=20)

        # ir cut

        self.button = customtkinter.CTkButton(master=self, command=self.ir_cut, text="IR Cut")
        self.button.grid(row=3, column=2, padx=20, pady=20)

    def zoom_slider(self, value):
            zoom_amt = value/100 * 20000

            info = {'PTZ_ZOOM': f'ON_{round(zoom_amt)}'}
            x_as_bytes = pickle.dumps(info)
            server.sendto((x_as_bytes), (SERVER, CMDPORT))
    
    def focus_slider(self, value):
            
            focus_amt = value/100 * 20000

            info = {'PTZ_FOCUS': f'ON_{round(focus_amt)}'}
            x_as_bytes = pickle.dumps(info)
            server.sendto((x_as_bytes), (SERVER, CMDPORT))

    def more_zoom(self):
        info = {'PTZ_ZOOM': '+'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    def less_zoom(self):
        info = {'PTZ_ZOOM': '-'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    def more_focus(self):
        info = {'PTZ_FOCUS': '+'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    def less_focus(self):
        info = {'PTZ_FOCUS': '-'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))
        
    def auto_focus(self):
        info = {'PTZ_FOCUS': 'AUTO'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    def servo_left(self):
        info = {'PTZ_MOVEMENT': 'LEFT'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    def servo_right(self):
        info = {'PTZ_MOVEMENT': 'RIGHT'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))
    
    def servo_up(self):
        info = {'PTZ_MOVEMENT': 'UP'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

    def servo_down(self):
        info = {'PTZ_MOVEMENT': 'DOWN'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))
    
    def ir_cut(self):
        info = {'IR_CUT': 'True'}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))

class App(customtkinter.CTk):

    customtkinter.set_appearance_mode("dark")
    global rec_toggle, video_screen_dim, image_x, image_y
    rec_toggle = False
    video_screen_dim = (1280, 720)
    image_x = 0
    image_y = 0
   
    def __init__(self):
        super().__init__()

        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        # self.geometry("{}x{}-{}+0".format(width, height, width + 8)) # added 8 pixels translation due to weird scaling :/
        self.geometry("{}x{}+0+0".format(width, height)) # added 8 pixels translation due to weird scaling :/
        self.title("Video Panel")
        self.wm_iconbitmap(default=None)

        # logo 

        kgb_logo = customtkinter.CTkImage(Image.open("ProductionCode\KGB_Logo.png"), size=(160, 75))
        logo = customtkinter.CTkLabel(self, text="", image=kgb_logo)
        logo.grid(row=5, column=20, sticky="ne")

        # 20x20 grid system

        self.grid_rowconfigure(tuple(range(21)), weight=1)
        self.grid_columnconfigure(tuple(range(21)), weight=1)
        
        # Camera buttons

        self.frame = CameraButtonGroup(master=self)
        self.frame.grid(row=2, column=0, columnspan=1 ,padx=(20, 20), pady=20, sticky='w')

        # PTZ buttons

        self.frame = PTZButtonGroup(master=self)
        self.frame.grid(row=3, column=0, rowspan=1, columnspan=1, padx=(20, 20), pady=20, sticky='ew')
    
        # window buttons

        self.button = customtkinter.CTkButton(master=self, command=self.max_window, text="Maximize")
        self.button.grid(row=0, column=18, padx=(200, 0), pady=20, sticky="e")

        self.button = customtkinter.CTkButton(master=self, command=self.mini_window, text="Minimize")
        self.button.grid(row=0, column=19, padx=(40, 0), pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.close_window, text="Close")
        self.button.grid(row=0, column=20, padx=(0, 20), pady=20, sticky="e")
        
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
        self.combobox = customtkinter.CTkComboBox(master=self, values=["ARDUCam.", "PTZ Cam."],
                                            command=self.combobox_callback)
        self.combobox.set('Select Camera')
        self.combobox.grid(row=2, column=0, pady=(200, 0), ipadx=10,sticky="ne")

        # video device 
        self.vid = VideoCaptureDevice('http://192.168.0.19:9000/stream.mjpg')
        self.canvas = tk.Canvas(self, width=1280, height=625, bg='gray', highlightthickness=0) #adjusted height by -95px to remove whitespace :/
        self.canvas.grid(row=1, column=1, rowspan=4, columnspan=20,padx=20, pady=20,sticky="nsew")
        self.video_update()
        # info resetter

        self.info_reset()

    def combobox_callback(self, choice):
        if choice == 'PTZ Cam.':
            self.vid = VideoCaptureDevice('http://192.168.0.19:9100/stream.mjpg') 

        elif choice == 'ARDUCam.':
            self.vid = VideoCaptureDevice('http://192.168.0.19:9000/stream.mjpg')

    def video_update(self):

        try:
            ret, frame = self.vid.get_frame()        
            if ret:
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(image_x, image_y, image=self.photo, anchor=tk.NW)  
            self.after(1, self.video_update)
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
        info = {'PTZ_ZOOM': '', 'PTZ_FOCUS': '', 'PTZ_MOVEMENT': '', 'IR_CUT': ''}
        x_as_bytes = pickle.dumps(info)
        server.sendto((x_as_bytes), (SERVER, CMDPORT))
        self.after(50, self.info_reset)

if __name__ == "__main__":
    app = App()
    app.mainloop()