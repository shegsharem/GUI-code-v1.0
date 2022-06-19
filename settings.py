import tkinter as tk
from tkinter import RAISED, GROOVE
from tkinter import ttk
import pygame

from fileget import Files

f = Files('data/settings/gamesettings.json')
loadedFile = f.readSettingsFile()

class Settings(tk.Frame):
    # Create a single window app
    def __init__(self, parent=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.max_res = Settings.getScreenData(self)

        self.lastgamewidth = f.readEntryFromSettingsFile(loadedFile,'settings','window_w')
        self.lastgameheight = f.readEntryFromSettingsFile(loadedFile,'settings','window_h')
    
        self.lastgame_res = (str(self.lastgamewidth)+'x'+str(self.lastgameheight))

        self.GAME_RESOLUTION = tk.StringVar()
        self.GAME_SET_FULLSCREEN = tk.StringVar()

        self.resolutionlist = [self.lastgame_res,
            str(loadedFile['settings']['max_window_w'])+ 'x'+str(loadedFile['settings']['max_window_h']),
             '1024x576',
             '1152x648',
             '1280x720',
             '854x480',
             '640x360',
             '426x240'
             ]
    
        self.GAME_RESOLUTION.set(self.resolutionlist[0])
        self.GAME_SET_FULLSCREEN.set(str(loadedFile['settings']['fullscreen']))


        # Define Window Stuff
        self.root.title('Settings') # Set window title
        self.root.resizable(False,False) # Not resizeable
        self.root.configure(bg="#FFFFFF")
        self.root.iconbitmap('data/icons/settings.ico')

        # Define window dimensions
        self.window_width = 300
        self.window_height = 110

        # Get centered coordinates of the display

        # Set resolution
        self.root.geometry((str(self.window_width)+"x"+str(self.window_height)))

        self.root.attributes('-top') # Launch on top layer
        self.root.eval('tk::PlaceWindow . center')

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

        self.ok_button = tk.Button(self.root, text='Ok',command=self.on_closing, relief=RAISED,borderwidth=2)
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

        self.root.focus()
        
    def on_closing(self):
        Settings.changeFullScreenSetting(self)
        f.writeSettingsFile(loadedFile)
        print("Saved Changes")
        self.root.destroy()
    
    
    def changeResolutionSetting(self, event=None):
        self.selected = self.GAME_RESOLUTION.get()
        print(self.selected)
        dimensions = self.selected.split("x")
        loadedFile['settings']['window_w'] = dimensions[0]
        loadedFile['settings']['window_h'] = dimensions[1]
    
    def changeFullScreenSetting(self):
        self.selected = self.GAME_SET_FULLSCREEN.get()
        loadedFile['settings']['fullscreen'] = self.selected
        

    def getScreenData(self):
        pygame.init()
        screendata = pygame.display.Info()
        loadedFile['settings']['max_window_w'] = str(screendata.current_w)
        loadedFile['settings']['max_window_h'] = str(screendata.current_h)
        f.writeSettingsFile(loadedFile)
        return (str(screendata.current_w)+'x'+str(screendata.current_h))
            

def main():
    root = tk.Tk()
    
    root.protocol("WM_DELETE_WINDOW", Settings(root).on_closing)
    root.mainloop()



if __name__ == "__main__":
    main()