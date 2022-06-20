import tkinter
import pygame

class Mbox(object):

    root = None

    def __init__(self, msg, dict_key):
        """
        msg = <str> the message to be displayed
        dict_key = <sequence> (dictionary, key) to associate with user input
        (providing a sequence for dict_key creates an entry for user input)
        """
        tki = tkinter
        pygame.init

        self.top = tki.Toplevel(Mbox.root)
        self.entry_to_dict = ''



        frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
        frm.pack(fill='both', expand=True)

        label = tki.Label(frm, text=msg)
        label.pack(padx=4, pady=4) 


            

        b_choose = tki.Button(frm, text='Choose Button')
        b_choose['command'] = self.top.destroy
        b_choose.pack(padx=4, pady=4)
    
    def getButtonInput(self):

