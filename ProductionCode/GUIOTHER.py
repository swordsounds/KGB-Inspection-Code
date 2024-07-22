import cv2, tkinter as tk, customtkinter # type: ignore
from PIL import Image, ImageTk # type: ignore
from datetime import datetime
import uuid

class VideoCaptureDevice:
    #highest res on pi is 1280, 720 using usb
    def __init__(self, video_link):
        self.vid = cv2.VideoCapture(video_link) #change ip in prod 192.168.0.19
        self.rec = None

    def get_frame(self) -> tuple[bool, list[int]]:
        ret, frame = self.vid.read()
        if rec_toggle:
                self.rec.write(frame)
        resized = cv2.resize(frame, video_screen_dim, interpolation=cv2.INTER_AREA)
        return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
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

class App(customtkinter.CTk):

    customtkinter.set_appearance_mode("dark")
    global rec_toggle, video_screen_dim
    rec_toggle = False
    video_screen_dim = (1280, 720)
   
    def __init__(self):
        super().__init__()

        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("{}x{}-{}+0".format(width, height, width + 8))
        self.title("Control Panel")
        self.wm_iconbitmap(default=None)
        # self.minsize(width, height)
        '''
        Background code, gotta fix buttons corner radius
        '''
        # background_image = customtkinter.CTkImage(Image.open("carbon-fiber-manufacturing-848x500.jpg"), size=(width, height))
        # bg_lbl = customtkinter.CTkLabel(self, text="", image=background_image)
        # bg_lbl.place(x=0, y=-1)

        # 20x20 grid system

        self.grid_rowconfigure(tuple(range(21)), weight=1)
        self.grid_columnconfigure(tuple(range(21)), weight=1)

        # window buttons

        self.button = customtkinter.CTkButton(master=self, command=self.max_window, text="Maximize")
        self.button.grid(row=0, column=18, padx=(200, 0), pady=20, sticky="e")

        self.button = customtkinter.CTkButton(master=self, command=self.mini_window, text="Minimize")
        self.button.grid(row=0, column=19, padx=(40, 0), pady=20)

        self.button = customtkinter.CTkButton(master=self, command=self.close_window, text="Close")
        self.button.grid(row=0, column=20, padx=(0, 20), pady=20, sticky="e")
        
        # video buttons
        self.label = customtkinter.CTkLabel(self, text="Video Settings")
        self.label.grid(row=1, column=4, padx=20, pady=(50, 0), sticky="se")

        self.record_on = customtkinter.CTkButton(master=self, command=self.program_take_recording, text="Rec.")
        self.record_on.grid(row=2, column=4, padx=0, pady=(0,50), sticky="ne")

        self.record_off = customtkinter.CTkButton(master=self, command=self.program_stop_recording, text="Stop Rec.")
        self.record_off.grid(row=2, column=4, padx=0, pady=0, sticky="e")

        self.button = customtkinter.CTkButton(master=self, command=self.program_take_picture, text="Take Pic.")
        self.button.grid(row=2, column=4, padx=0, pady=(50, 0), sticky="se")

        # video selector 
        

        self.combobox = customtkinter.CTkComboBox(master=self, values=["camera 1", "camera 2", "camera 3", "camera 4"],
                                            command=self.combobox_callback)
        self.combobox.set('camera 3')
        self.combobox.grid(row=3, column=4, sticky="e")

        # video device 

        
        self.canvas = tk.Canvas(self, width=1280, height=700, bg='gray', highlightthickness=0) #adjusted height by -20px to remove whitespace :/
        self.canvas.grid(row=1, column=4, rowspan=4, columnspan=20,padx=20, pady=20,sticky="nse")
        self.video_update() 
        
        # fullscreen after elements loaded
        # self.wm_attributes('-fullscreen', True) # uncomment in prod
        
    def combobox_callback(self, choice):
        if choice == 'camera 2':
            self.vid = VideoCaptureDevice('http://192.168.0.19:9000/stream.mjpg')
            self.video_update() 
          
        elif choice == 'camera 3':
            self.vid = VideoCaptureDevice('http://192.168.0.19:9001/stream.mjpg')
            self.video_update() 

    def video_update(self):
        try:
            ret, frame = self.vid.get_frame()        
            if ret:
                    self.photo = ImageTk.PhotoImage(image= Image.fromarray(frame))
                    self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)  
            self.after(1, self.video_update)
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

    def max_window(self):
        # self.wm_attributes("-fullscreen", "True")
        self.geometry("{}x{}-{}+0".format(1920, 1080, 1928))
        
    def mini_window(self):
        # self.wm_attributes("-fullscreen", "False")
        self.geometry("{}x{}-{}+0".format(300, 300, 1925))
    
    def close_window(self):
        self.destroy()
if __name__ == "__main__":
    app = App()
    app.mainloop()