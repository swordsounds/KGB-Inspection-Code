import customtkinter
from datetime import datetime

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

        self.time = customtkinter.CTkTextbox(master=self, width=100,height=10, font=("", 20))
        self.time.grid(row=0, column=0, padx=0, pady=20, sticky=None)
        self.time.insert("0.0", 'CURRENTTIME')

        # display placeholder 

        self.video_feed = customtkinter.CTkTextbox(master=self)
        self.video_feed.grid(row=1, column=3, rowspan=8, columnspan=8, padx=20, pady=(0, 20), sticky="nsew")
        self.video_feed.insert("0.0", "VIDEO_OFFLINE")
        # options tabs

        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=1, column=2, padx=20, pady=20)

        # window buttons

        x_window_group: int = 8
        y_window_group: int = 0

        self.button = customtkinter.CTkButton(master=self, command=self.max_window, text="Maximize")
        self.button.grid(row=y_window_group, column=x_window_group, padx=180, pady=20, sticky="w")

        self.button = customtkinter.CTkButton(master=self, command=self.mini_window, text="Minimize")
        self.button.grid(row=y_window_group, column=x_window_group, padx=(170, 0), pady=20, sticky=None)

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
        self.button.grid(row=y_gripper_group, column=x_gripper_group, padx=10, pady=40, sticky="ne")
        
        self.button = customtkinter.CTkButton(master=self, command=None, text="Claw Close")
        self.button.grid(row=y_gripper_group, column=x_gripper_group, padx=10, pady=40, sticky="nw")

        self.button = customtkinter.CTkButton(master=self, command=None, text="Claw Right")
        self.button.grid(row=y_gripper_group, column=x_gripper_group, padx=10, pady=40, sticky="se")
        
        self.button = customtkinter.CTkButton(master=self, command=None, text="Claw Left")
        self.button.grid(row=y_gripper_group, column=x_gripper_group, padx=10, pady=40, sticky="sw")

        # arm buttons

        x_arm_group: int = 2
        y_arm_group: int = 4

        self.button = customtkinter.CTkButton(master=self, command=None, text="Extend Arm")
        self.button.grid(row=y_arm_group, column=x_arm_group, padx=20, pady=0, sticky="n")

        self.button = customtkinter.CTkButton(master=self, command=None, text="Retract Arm")
        self.button.grid(row=y_arm_group, column=x_arm_group, padx=20, pady=0, sticky="s")

        self.time_start()

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

   
# print(help(App))

if __name__ == "__main__":
    app = App()
    app.attributes("-fullscreen", "True")
    app.mainloop()