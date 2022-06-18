from tkinter.colorchooser import askcolor # used for color chooser
import json

from click import edit


class editThemeFile:
    def __init__(self) -> None:
        self.themeFile = ''
        self.loadedFile = {}
        self.originalcolor = ''
        self.colorToBeChanged = ''

    def openjson(self):
        # Read json
        themeFile = open(self.themeFile, 'r')
        self.loadedFile = json.load(themeFile)
        themeFile.close()
    
    def savetojson(self):
        themeFile = open(self.themeFile, 'w')
        print(self.loadedFile['default']['colours'][self.colorToBeChanged])
        json.dump(self.loadedFile, themeFile, indent=4)
        themeFile.close()

    def colorprompt(self):
        editThemeFile.openjson(self)
        self.originalcolor = self.loadedFile['default']['colours'][self.colorToBeChanged]

        self.colorChoice = askcolor(color=(self.loadedFile['default']['colours'][self.colorToBeChanged]), title="Choose Color")
        if self.colorChoice[1] == None:
            self.loadedFile['default']['colours'][self.colorToBeChanged] = self.originalcolor
        else:
            self.loadedFile['default']['colours'][self.colorToBeChanged] = self.colorChoice[1]
        editThemeFile.savetojson(self)


editTheme = editThemeFile()

def run():
    editTheme.themeFile = 'theme.json'
    editTheme.openjson()
    print(editTheme.loadedFile)
    editTheme.colorToBeChanged = 'normal_bg'
    editTheme.colorprompt()

if __name__ == '__main__':
    run()