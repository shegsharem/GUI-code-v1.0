from re import S
from telnetlib import SE
import tkinter as tk
from tkinter import NS, messagebox
from tkinter import simpledialog
from tkinter import ttk, OptionMenu

from tkinter.font import BOLD
from tkinter.ttk import Style

import json
from turtle import bgcolor, update






class Settings(tk.Frame):
    # Create a single window app
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent

        self.settingsFile = 'data/settings/gamesettings.json'
        #self.loadedFile = {}
        #self.loadedFileNonChanged = {}
    
        Settings.openSettingsFile(self)
        
        

        self.GAME_RESOLUTION = tk.StringVar()

        self.resolutionlist = [str(self.loadedFile['settings']['window_w'])+ 'x'+str(self.loadedFile['settings']['window_h']), 
            '1980x1280', '840x680']
        self.GAME_RESOLUTION.set(self.resolutionlist[0])

        #self.GAME_RESOLUTION.set(str(self.loadedFile['settings']['window_w'])+ 'x'+str(self.loadedFile['settings']['window_h']))


        # Define Window Stuff
        self.root.title('Settings') # Set window title
        self.root.resizable(False,False) # Not resizeable
        self.root.configure(bg="#FFFFFF")
        self.root.iconbitmap('data/icons/settings.ico')

        # Define window dimensions
        self.window_width = 500
        self.window_height = 400

        # Get screen dimensions of computer
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.center_x = int(self.screen_width/2 - self.window_width / 2)
        self.center_y = int(self.screen_height/2 - self.window_height / 2)

        # Set resolution
        self.root.geometry(f'{self.window_width}x{self.window_height}+{self.center_x}+{self.center_y}')

        self.root.attributes('-top',1) # Launch on top layer

        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=0)
        self.root.columnconfigure(2, weight=5)

        self.create_widgets()
        # ---------------------------------------- GUI OBJECTS -----------------------------------------------------------------
    def create_widgets(self):
        parent = self.root
        self.Title = ttk.Label(self.root, text='Settings',font=('', 12, BOLD),background="#FFFFFF",foreground="#000000")
        self.Title.grid(column=0, row=0, sticky=tk.NW, padx=5, pady=5)



        self.BLabel = ttk.Label(self.root, text=('Window Resolution'), font=('',11),background='#FFFFFF')
    
        self.resolution = ttk.Combobox(self.root, values=self.resolutionlist, textvariable=self.GAME_RESOLUTION)
        self.BLabel.grid(column=0, row=1,sticky=tk.NS,padx=5,pady=5)
        self.resolution.grid(column=1, row=1,sticky=tk.NS, padx=5,pady=0)
        
        self.ok_button = ttk.Button(self.root, text='Ok',command=self.on_closing)
        self.ok_button.grid(column=2,row=5, sticky=tk.E, padx=0,pady=305)

        self.cancel_button = ttk.Button(self.root, text='Cancel', command=self.root.destroy)
        self.cancel_button.grid(column=3,row=5, sticky=tk.W, padx=10,pady=5)
    
        
        

        self.resolution.bind('<<ComboboxSelected>>',lambda event: self.changeResolutionSetting())
    
    

        self.style = Style()
        self.style.configure('TNotebook', background='#FFFFFF')
       

    def on_closing(self):
        Settings.saveSettingsFile(self)
        print("Saved Changes")
        self.root.destroy()
    
    
    def changeResolutionSetting(self, event=None):
        self.selected = self.GAME_RESOLUTION.get()
        print (self.selected)
            #print(self.resolutionlist)
        

        dimensions = self.selected.split("x")
        self.loadedFile['settings']['window_w'] = dimensions[0]
        self.loadedFile['settings']['window_h'] = dimensions[1]


    def openSettingsFile(self):
        # Read json
        settingsFile = open(self.settingsFile, 'r')
        self.loadedFile = json.load(settingsFile)
        settingsFile.close()
        

    def saveSettingsFile(self):        
        settingsFile = open(self.settingsFile, 'w')
            #print(self.loadedFile)
        json.dump(self.loadedFile, settingsFile, indent=4)
        settingsFile.close()
        return print("Saved")

    
            
            
        


        
            

def main():
    root = tk.Tk()
    
    root.protocol("WM_DELETE_WINDOW", Settings(root).on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()