#from game import Game
from startup import Settings, GUI

#g = Game()
s = Settings()
gui = GUI()

while s.running:
    #g.playing = True
    #g.game_loop()
    gui.run()
    s.run()

