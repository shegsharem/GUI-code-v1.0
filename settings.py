import tkinter as tk
from tkinter import RAISED, SUNKEN, FLAT, RIDGE, GROOVE, SOLID
from tkinter import simpledialog
from tkinter import ttk, OptionMenu



import json







class Settings(tk.Frame):
    # Create a single window app
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent

        self.settingsFile = 'data/settings/gamesettings.json'
        #self.loadedFile = {}
        #self.loadedFileNonChanged = {}

        self.user_screen_width = self.root.winfo_screenwidth()
        self.user_screen_height = self.root.winfo_screenheight()

        self.user_max_resolution = (str(self.user_screen_width)+'x'+str(self.user_screen_height))
    
        Settings.openSettingsFile(self)
        
        

        self.GAME_RESOLUTION = tk.StringVar()
        self.GAME_SET_FULLSCREEN = tk.StringVar()

        self.resolutionlist = [
            str(self.loadedFile['settings']['window_w'])+ 'x'+str(self.loadedFile['settings']['window_h']), 
            self.user_max_resolution,
             '840x680',
             '375x667',
             '360x640'
             ]
    
        self.GAME_RESOLUTION.set(self.resolutionlist[0])
        self.resolutionlist.sort()
        self.GAME_SET_FULLSCREEN.set(str(self.loadedFile['settings']['fullscreen']))
        print("Fullscreen=",str(self.loadedFile['settings']['fullscreen']))
        #self.GAME_RESOLUTION.set(str(self.loadedFile['settings']['window_w'])+ 'x'+str(self.loadedFile['settings']['window_h']))


        # Define Window Stuff
        self.root.title('Settings') # Set window title
        self.root.resizable(False,False) # Not resizeable
        self.root.configure(bg="#FFFFFF")
        self.root.iconbitmap('data/icons/settings.ico')

        # Define window dimensions
        self.window_width = 300
        self.window_height = 110

        # Get centered coordinates of the display

        self.center_x = int(self.user_screen_width/2 - self.window_width/2)
        self.center_y = int(self.user_screen_height/2 - self.window_height/2)

        # Set resolution
        self.root.geometry(f'{self.window_width}x{self.window_height}+{self.center_x}+{self.center_y}')

        self.root.attributes('-top') # Launch on top layer

        self.frame1 = ttk.Frame(self.root, relief=GROOVE, borderwidth=2)
        self.frame1.pack(fill='x', expand=True,padx=3,pady=3)
        self.frame2 = ttk.Frame(self.frame1)
        self.frame2.pack(fill='x',expand=True)
        

        self.create_widgets()
        # ---------------------------------------- GUI OBJECTS -----------------------------------------------------------------
    def create_widgets(self):
        parent = self.root

        self.fullscreen_checkbutton = tk.Checkbutton(self.frame2, variable=self.GAME_SET_FULLSCREEN,
            onvalue="1",offvalue="0")
        self.fullscreen_label_checkbutton = tk.Label(self.frame2, text="Fullscreen")
        

        self.resolution = ttk.Combobox(self.frame1, values=self.resolutionlist, textvariable=self.GAME_RESOLUTION, state='readonly')  
        self.ResolutionLabel = tk.Label(self.frame1, text=('Game Resolution'))

        self.ok_button = tk.Button(self.root, text='Save',command=self.on_closing, relief=RAISED,borderwidth=2)
        self.cancel_button = tk.Button(self.root, text='Cancel', command=self.root.destroy, relief=RAISED, borderwidth=2)

        # ----------------------------- PACKING ----------------------------------------------
        self.fullscreen_checkbutton.pack(side='right')
        self.fullscreen_label_checkbutton.pack(side='left',padx=5,pady=5)

        self.resolution.pack(side='right',padx=5,pady=5)
        self.ResolutionLabel.pack(side='left',padx=5,pady=5)

        self.cancel_button.pack(side='right',padx=5,pady=5,ipadx=15)
        self.ok_button.pack(side='right',ipadx=30,pady=5)

        # -------------------------------------------------------------------------------------
        self.resolution.bind('<<ComboboxSelected>>',lambda event: self.changeResolutionSetting())

        
    def on_closing(self):
        Settings.changeFullScreenSetting(self)
        Settings.saveSettingsFile(self)
        print("Saved Changes")
        self.root.destroy()
    
    
    def changeResolutionSetting(self, event=None):
        self.selected = self.GAME_RESOLUTION.get()
        print(self.selected)
            #print(self.resolutionlist)
        

        dimensions = self.selected.split("x")
        self.loadedFile['settings']['window_w'] = dimensions[0]
        self.loadedFile['settings']['window_h'] = dimensions[1]
    
    def changeFullScreenSetting(self):
        self.selected = self.GAME_SET_FULLSCREEN.get()
        self.loadedFile['settings']['fullscreen'] = self.selected


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