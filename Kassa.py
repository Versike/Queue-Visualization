from tkinter import IntVar
class Kassa():
    def __init__(self):
        self.number = None
        self.queue = []
        self.x = 0
        self.y = 0
        self.delay = []
        self.mean = 0
        self.countOfDelay = 0
        self.tck1 = IntVar(value=1)
        self.tck2 = IntVar(value=8)