import json
from functools import reduce

class Files():
    def __init__(self,jsonfilepath):
        self.settingsFile = jsonfilepath

    # When calling this object you should save the returned value to a variable
    def readSettingsFile(self):
        settingsFile = open(self.settingsFile, 'r')
        self.loadedFile = json.load(settingsFile)
        settingsFile.close()
        return self.loadedFile
    
    # dict is the dictionary you want to save
    def writeSettingsFile(self, dict):
        settingsFile = open(self.settingsFile, 'w')
        json.dump(dict, settingsFile, indent=4)
        settingsFile.close()
        return
    
    def readEntryFromSettingsFile(self, dict, *entries):
        result =  reduce(lambda d, key: d.get(key) if d else None, entries, dict)
        return result

if __name__ == '__main__':
    getFile = Files("data/settings/gamesettings.json")
    yett = getFile.readSettingsFile()
    print(yett)
    getFile.writeSettingsFile(yett)
    entry = getFile.readEntryFromSettingsFile(yett, 'settings','fullscreen')
    print(entry)