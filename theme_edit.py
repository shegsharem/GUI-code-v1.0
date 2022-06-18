from tkinter.colorchooser import askcolor # used for color chooser
import json

from click import edit


class editThemeFile:
    def __init__(self) -> None:
        self.themeFile = ''
        self.loadedFile = {}
        self.originalcolor = ''
        self.colorToBeChanged = ''
        self.path = ''

    def openjson(self):
        # Read json
        themeFile = open(self.themeFile, 'r')
        self.loadedFile = json.load(themeFile)
        themeFile.close()
    
    def savetojson(self):
        themeFile = open(self.themeFile, 'w')
        path = self.path.split(',')
        print(self.loadedFile[path[0]][path[1]][path[2]])
        json.dump(self.loadedFile, themeFile, indent=4)
        themeFile.close()

    def colorprompt(self):
        editThemeFile.openjson(self)
        path = self.path.split(',')
        print(path)
        print(self.loadedFile[path[0]][path[1]][path[2]])
        self.originalcolor = self.loadedFile[path[0]][path[1]][path[2]]
            

        self.colorChoice = askcolor(color=(self.loadedFile[path[0]][path[1]][path[2]]), title="Choose Color")
        if self.colorChoice[1] == None:
            self.loadedFile[path[0]][path[1]][path[2]] = self.originalcolor
        else:
            self.loadedFile[path[0]][path[1]][path[2]] = self.colorChoice[1]
        editThemeFile.savetojson(self)


editTheme = editThemeFile()

def run():
    editTheme.themeFile = 'theme.json'
    editTheme.openjson()
    print(editTheme.loadedFile)
    # List layers of json to be changed seperated by a comma
    #editTheme.path = 'default,colours,normal_bg'
    buttonNormalBackground = 'buttons,colours,normal_bg'
    editTheme.path = buttonNormalBackground
    editTheme.colorprompt()

    

if __name__ == '__main__':
    run()