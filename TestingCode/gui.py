import customtkinter

class App(customtkinter.CTk):
    # customtkinter.set_default_color_theme("dark-blue")
    customtkinter.set_appearance_mode("dark")

    def __init__(self):
        super().__init__()

        self.geometry("500x300")
        self.title("small example app")
        # self.wm_iconbitmap(default=None)
        self.minsize(300, 200)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="nsew")

        self.combobox = customtkinter.CTkComboBox(master=self, values=["Sample text 1", "Text 2"])
        self.combobox.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.button = customtkinter.CTkButton(master=self, command=self.button_callback, text="Insert Text")
        self.button.grid(row=0, column=2, padx=20, pady=20, sticky="new")

    def button_callback(self):
        self.textbox.insert("insert", self.combobox.get() + "\n")


# print(help(App))

if __name__ == "__main__":
    app = App()
    # app.attributes("-fullscreen", "True")
    # app.state('zoomed')
    app._state_before_windows_set_titlebar_color = 'zoomed'

    # width = app.winfo_screenwidth()
    # height = app.winfo_screenheight()
    # geometry = str(width) + "x" + str(height)
    # app.geometry(geometry)
    app.mainloop()