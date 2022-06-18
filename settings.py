import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from theme_edit import editThemeFile






class Settings(tk.Frame):
    # Create a single window app
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        

        # Define Window Stuff
        self.root.title('Settings') # Set window title
        self.root.resizable(False,False) # Not resizeable
        self.root.configure(bg="#303030")
        self.root.iconbitmap('data/icons/settings.ico')

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

        self.root.attributes('-top',1) # Launch on top layer

        # ---------------------------------------- GUI OBJECTS -----------------------------------------------------------------
        self.Title = ttk.Label(self.root, text='Settings',font=('', 24),background="#303030",foreground="#FFFFFF")
        self.B = ttk.Button(self.root, text='Change Resolution', command=Settings.settingChange)



        self.Title.pack(ipadx=10,ipady=10)
        self.B.pack(ipadx=10,ipady=10)
        self.B.place(relx=0.2,rely=0.1,anchor='center')
        self.Title.place(relx=0.1,rely=0.05, anchor='center')
        

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

    def settingChange():
        editTheme = editThemeFile()
        editTheme.themeFile = 'theme.json'
        editTheme.openjson()
        print(editTheme.loadedFile)
        editTheme.path = 'default,colours,normal_bg'
        editTheme.colorprompt()
            
            
        


        
            

def main():
    root = tk.Tk()
    Settings(root).pack(side='top', expand=True)
    root.protocol("WM_DELETE_WINDOW", Settings(root).on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()