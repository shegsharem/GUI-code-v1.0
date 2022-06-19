import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk, OptionMenu

from tkinter.font import BOLD
from tkinter.ttk import Style

import json
from turtle import update






class Settings(tk.Frame):
    # Create a single window app
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent

        self.settingsFile = 'data/settings/gamesettings.json'
        self.loadedFile = {}
        self.loadedFileNonChanged = {}
    
        Settings.openSettingsFile(self)

        self.GAME_RESOLUTION = tk.StringVar()

        self.GAME_RESOLUTION.set(str(self.loadedFile['settings']['window_w'])+ ' x '+str(self.loadedFile['settings']['window_h']))
        self.GAME_RESOLUTION.trace('w',None)

        Settings.saveSettingsFile(self)

        # Define Window Stuff
        self.root.title('Settings') # Set window title
        self.root.resizable(False,False) # Not resizeable
        self.root.configure(bg="#FFFFFF")
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
        self.Title = ttk.Label(self.root, text='Settings',font=('Consolas', 24, BOLD),background="#FFFFFF",foreground="#000000")
        

        self.menuRibbon = ttk.Notebook(parent, style='TNotebook')

        
        
        self.menuRibbon.pack(pady=10, expand=True)
        self.Title.pack(ipadx=10,ipady=10)
        self.Title.place(relx=0.12,rely=0.05, anchor='center')

        self.frame1 = ttk.Frame(self.menuRibbon, width=750, height=450)
        self.frame2 = ttk.Frame(self.menuRibbon, width=750, height=450)

        self.frame1.pack(fill='both', expand=True)

        self.menuRibbon.add(self.frame1, text="General",)
        self.menuRibbon.add(self.frame2, text="Graphics")

        self.B = tk.Button(self.frame2, text='Change Window Width',
            command=lambda : Settings.settingsNumChanger(self,'settings,window_w', 'Change Window Width'))
        
        self.BLabel = ttk.Label(self.frame2, textvariable= self.GAME_RESOLUTION,
            font=('Consolas', 14, BOLD),background="#EEEEEE",foreground="#000000")
        
        self.B1 = tk.Button(self.frame2, text=('Change Window Height'),
            command=lambda : Settings.settingsNumChanger(self,'settings,window_h', 'Change Window Height'))
        
        self.B.pack(ipadx=10,ipady=10, fill='both')
        self.B1.pack(ipadx=10,ipady=10)
        self.BLabel.pack(ipadx=10,ipady=10)

        
        
        self.B.place(relx=0.2,rely=0.12,anchor='center')
        self.B1.place(relx=0.2,rely=0.22, anchor='center')
        self.BLabel.place(relx=0.2, rely=0.05, anchor='center')

        self.style = Style()
        self.style.configure('TNotebook', background='#FFFFFF')
       

    def on_closing(self):
        if self.loadedFile == self.loadedFileNonChanged:
            pass
        else:
            Settings.saveSettingsFile(self)
            print("Saved Changes")
        self.root.destroy()
    


    def openSettingsFile(self):
        # Read json
        settingsFile = open(self.settingsFile, 'r')
        self.loadedFile = json.load(settingsFile)
        self.loadedFileNonChanged = self.loadedFile
        settingsFile.close()
        

    def saveSettingsFile(self):        
        settingsFile = open(self.settingsFile, 'w')
            #print(self.loadedFile)
        json.dump(self.loadedFile, settingsFile, indent=4)
        settingsFile.close()
        return print("Saved")

           

            


    def settingsNumChanger(self, path, message):
        Settings.openSettingsFile(self)

        filepath = path.split(',')
        self.originalnum = self.loadedFileNonChanged[filepath[0]][filepath[1]]

        self.numInput = simpledialog.askinteger("Input", message, parent=self.root)
        if self.numInput is not None:
            self.loadedFile[filepath[0]][filepath[1]] = self.numInput.__str__()
            if self.originalnum.__str__() == self.loadedFile[filepath[0]][filepath[1]]:
                pass
            else:
                print("Changes made")
                Settings.saveSettingsFile(self)
                self.GAME_RESOLUTION.set(str(self.loadedFile['settings']['window_w'])+ ' x '+str(self.loadedFile['settings']['window_h']))

    
            
            
        


        
            

def main():
    root = tk.Tk()
    
    root.protocol("WM_DELETE_WINDOW", Settings(root).on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()