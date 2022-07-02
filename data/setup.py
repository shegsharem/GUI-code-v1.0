import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"includes": ["os", 'pygame','sys','random','pygame_gui','tkinter', 'time', 'pynput._win32'], "include_files": [
    'data/images/playerframes/player0.png','data/images/playerframes/player1.png',
    'data/images/playerframes/player2.png','data/images/playerframes/player3.png',
    'data/images/playerframes/player4.png','data/images/playerframes/player5.png',
    'data/images/playerframes/player6.png','data/images/terrain/dirt.png',
    'data/images/terrain/whitesquare.png','data/settings/gamesettings.json',
    'data/settings/theme.json','data/fonts/orange kid.ttf']}


# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="bloot",
    version="0.1",
    description="My GAME",
    options={"build_exe": {
            'build_exe': './/build'}},
    executables=[Executable("data/main.py", base=base)],
)