from tkinter import Tk, Text, Label, Button, Frame

# OPTIONS FOR INPUT TYPES
ENTRY = 'entry'
COMBO = 'combo'


class Window(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.left_frame = Frame(self)
        self.right_frame = Frame(self)
