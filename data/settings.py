import tkinter as tk
from tkinter import RAISED
from tkinter import ttk
import pygame
from pynput import keyboard

from fileget import Files

f = Files('data/settings/gamesettings.json')
loadedFile = f.readSettingsFile()

def getScreenData():
        pygame.init()
        screendata = pygame.display.Info()
        loadedFile['settings']['max_window_w'] = str(screendata.current_w)
        loadedFile['settings']['max_window_h'] = str(screendata.current_h)
        f.writeSettingsFile(loadedFile)
        return (str(screendata.current_w)+'x'+str(screendata.current_h))


class Settings(tk.Frame):
    # Create a single window app
    def __init__(self, parent=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent

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
        sorted(self.resolutionlist, key=lambda x: int(x.split('x')[1]), reverse=True) # sort resolutions based on height
        self.GAME_SET_FULLSCREEN.set(str(loadedFile['settings']['fullscreen']))


        # Define Window Stuff
        self.root.title('Settings') # Set window title
        self.root.resizable(False,False) # Not resizeable
        self.root.configure(bg="#FFFFFF")

        # Define window dimensions
        self.window_width = 400
        self.window_height = 275

        # Get centered coordinates of the display
        self.root.eval('tk::PlaceWindow . center')
        # Set resolution
        self.root.geometry((str(self.window_width)+"x"+str(self.window_height)))

        self.root.attributes('-top') # Launch on top layer
        

        self.notebook = ttk.Notebook(self.root)

        self.frame1 = ttk.Frame(self.notebook, relief=RAISED, borderwidth=2)
        self.frame1.pack(fill='x', expand=True,padx=3,pady=3)
        self.frame2 = ttk.Frame(self.frame1)
        self.frame2.pack(fill='x',expand=True)
        self.frame3 = ttk.Frame(self.notebook, relief=RAISED, borderwidth=2)
        
        self.notebook.add(self.frame1, text="Graphics")
        self.notebook.add(self.frame3, text="Controls")
        self.notebook.pack(expand=True,fill='x')

        self.create_widgets()
        # ---------------------------------------- GUI OBJECTS -----------------------------------------------------------------
    def create_widgets(self):
        parent = self.root

        self.fullscreen_checkbutton = tk.Checkbutton(self.frame1, variable=self.GAME_SET_FULLSCREEN,
            onvalue="1",offvalue="0")
        self.fullscreen_label_checkbutton = tk.Label(self.frame1, text="Fullscreen")
        self.fullscreen_info = tk.Label(self.frame1, text="*Note, running in fullscreen \ngenerally has better performance")
        

        self.resolution = ttk.Combobox(self.frame2, values=self.resolutionlist, textvariable=self.GAME_RESOLUTION, state='readonly')  
        self.ResolutionLabel = tk.Label(self.frame2, text=('Game Resolution'))

        self.ok_button = tk.Button(self.root, text='Save',command=self.on_closing, relief=RAISED,borderwidth=2)
        self.cancel_button = tk.Button(self.root, text='Cancel', command=self.root.destroy, relief=RAISED, borderwidth=2)

        self.changecontrol_button = tk.Button(self.frame3, text='Change Control',relief=RAISED, borderwidth=2)
        self.changecontrol_button['command'] = lambda: items_selected() #change control button command

        self.ListboxScrollbar = tk.Scrollbar(self.frame3, orient=tk.VERTICAL)

        self.controlsListbox = ttk.Treeview(self.frame3,column=("Control", 'Key'),
            selectmode= tk.BROWSE, yscrollcommand=self.ListboxScrollbar.set,show='tree',cursor='')
        

        self.ListboxScrollbar.config(command=self.controlsListbox.yview)
        

        # ----------------------------- PACKING ----------------------------------------------
        self.ResolutionLabel.pack(side='left',padx=5,pady=5,expand=False)
        self.resolution.pack(side='left',padx=5,pady=5)

        self.fullscreen_label_checkbutton.pack(side='left',padx=5,pady=5)
        self.fullscreen_checkbutton.pack(side='left')
        self.fullscreen_info.pack(side='left',padx=10,pady=10)
        
        self.cancel_button.pack(side='right',padx=5,pady=5,ipadx=22, expand=False, fill='x')
        self.ok_button.pack(side='right',ipadx=30,pady=5,expand=False, fill='x')

        self.changecontrol_button.pack(side='right',padx=5,pady=5)
        self.controlsListbox.pack(side='left',padx=5,pady=5, expand=True, fill='both')
        self.ListboxScrollbar.pack(side='left',fill='both',)
        

        
        self.controlsList = loadedFile['settings']
        # Filter out keys in self.controlsList that contain 'button' and write to new dictionary, self.customControlsList
        self.customControlsList =  f.newDictFromKeySearch(self.controlsList,'button')
        
        for key in sorted(self.customControlsList):
            self.controlsListbox.insert('',tk.END, text=key,values=self.customControlsList[key])
            print(self.customControlsList)

        
        

        f.updateDictWithNewValues(self.controlsList,self.customControlsList)

        def items_selected(event=None):
            #handle item selected event
            # get selected indices
            selected_indices = {}
            selected_indices = self.controlsListbox.focus()
            # Collect events until released
            with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
                listener.join() 


            self.controlsListbox.insert(text=self.controlsListbox.item(selected_indices)['text'],parent='',
                index=selected_indices[3],values=(self.keyPressed))

            self.controlsListbox.delete(selected_indices)
            
        # -------------------------------------------------------------------------------------
        self.resolution.bind('<<ComboboxSelected>>',lambda event: self.changeResolutionSetting())
        #self.changecontrol_button.bind('<Return>', lambda event: items_selected())
        #self.controlsListbox.bind('<<TreeviewSelect>>', lambda event: items_selected())


        self.root.focus()
        
    def on_closing(self):
        Settings.changeFullScreenSetting(self)
        Settings.getCustomControls(self)
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
    
    def getCustomControls(self):
        self.value_dict = {}
        for x in self.controlsListbox.get_children():
            
            self.value_dict[str(self.controlsListbox.item(x)["text"])] = str(self.controlsListbox.item(x)["values"]).strip(' [\']')
            #values.append(value_dict)
        
        print("New Controls")
        print(self.value_dict)

        newList = f.updateDictWithNewValues(self.customControlsList,self.value_dict)
        print("NEW DICT")
        loadedFile['settings'] = f.updateDictWithNewValues(loadedFile['settings'],newList)
        print(loadedFile)

def on_press(key):
    try:
        Settings.keyPressed = (str(key.char))
        print (key.char)
    except AttributeError:
        ch = '.'
        key = str(key).lower()
        # Remove all characters before the character '-' from string
        before, sep, after = key.partition('.')
        if len(after) > 0:
            key = after
        print (key)
        if key == 'esc':
            key = 'escape'
        if key == 'enter':
            key = 'return'
        Settings.keyPressed = (str(key))
        

def on_release(key):
    return False
    

def main():
    root = tk.Tk()
    
    
    root.protocol("WM_DELETE_WINDOW", Settings(root).on_closing)
    root.mainloop()




if __name__ == "__main__":
    main()