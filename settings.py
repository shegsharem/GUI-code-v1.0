import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sys



class Settings:
    # Create a single window app
    def __init__(self):
        self.root = tk.Tk()
        Settings.running = True

        # Define Window Stuff
        self.root.title('Settings') # Set window title
        self.root.resizable(False,False) # Not resizeable
        self.root.configure(bg="#303030")

        # Define window dimensions
        self.window_width = 800
        self.window_height = 600

        # Get screen dimensions of computer
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.center_x = int(self.screen_width/2 - self.window_width / 2)
        self.center_y = int(self.screen_height/2 - self.window_height / 2)

        # Set resolution
        self.root.geometry(f'{self.window_width}x{self.window_height}+{self.center_x}+{self.center_y}')

        self.root.attributes('-topmost',-1) # Launch on top layer

        self.Title = ttk.Label(self.root, text='Settings', font=("Consolas",18),background="#303030",foreground="#FFFFFF")
        self.Title.pack(ipadx=10,ipady=10)
        self.Title.place(relx=0.1,rely=0.05, anchor='center')
        

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            Settings.running = False
            sys.exit()
            
            

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", Settings.on_closing)
        self.root.mainloop()

        
            

if __name__ == "__main__":
    Settings().run()