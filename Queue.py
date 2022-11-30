from tkinter import *
import random
from Kassa import Kassa

class Queue:
    def __init__(self, root):
        self.window = root
        self.window.config(bg="white")
        
        #Elements initialization
        self.kassaName = None
        self.startQueues = None
        self.nKassaAmount = None
        
        #Parameters
        self.QueuePersons = 0
        
        #Canvas settings
        self.canvasWidth = 700
        self.canvasHeight = 500
        
        self.queue_canvas = Canvas(self.window, width=self.canvasWidth, height=self.canvasHeight,bg="white", relief=RAISED, bd=10)
        self.queue_canvas.pack(fill=BOTH)
        
        #Call functions
        self.entryLabels()
        self.makeButtons()
        self.kassaParameters()
        
    #Labels for entry's elements
    def entryLabels(self):
        self.kassaAmount = Label(self.window, text = "N", fg = "black")
        self.kassaAmount.place(x=140, y=538)
        
        self.timeComePersons = Label(self.window, text = "T", fg = "black")
        self.timeComePersons.place(x=180, y=538)
        
        self.Persons = Label(self.window, text = "P", fg = "black")
        self.Persons.place(x=220, y=538)
        
    #Buttons settings    
    def makeButtons(self):
        self.startQueues = Button(self.window, text = "Start", fg = "Green", command = self.initKasses)
        self.startQueues.place(x=30, y=535)
        
        self.pauseQueues = Button(self.window, text = "Stop", fg = "red")
        self.pauseQueues.place(x=70, y=535)
    
    #Entry settings        
    def kassaParameters(self):
        self.nKassaAmount = Entry(self.window, fg = "black", bg = "white", width=2)
        self.nKassaAmount.place(x=150, y=540)
        
        self.tTimeComePersons = Entry(self.window, fg = "black", bg = "white", width=2)
        self.tTimeComePersons.place(x=190, y=540)

        self.pPersons = Entry(self.window, fg = "black", bg = "white", width=2)
        self.pPersons.place(x=230, y=540)
        
    #Function to make kasses
    def drawKassa(self, kassaNumber, x, y):
        #init name of kassa
        self.kassaName = Label(self.queue_canvas, text = "Касса " + str(kassaNumber), fg = "black")
        self.kassaName.place(x = x, y = y)
        self.kassaQueuePersons = Label(self.queue_canvas, text = self.QueuePersons, fg = "black")
        self.kassaQueuePersons.place(x = x, y = y + 20)
        
    #Main function to start queue
    def initKasses(self):
        kassaAmount = int(self.nKassaAmount.get())
        x = 20
        y = 0
        self.kassaLabel = []
        self.kasses = []
        for kassa in range(kassaAmount):
            labelKassa = self.drawKassa(kassa, x, y)
            self.kassaLabel.append(labelKassa)
            t = self.tTimeComePersons.get()
            p = self.pPersons.get()
                        
            obj = Kassa(tTimeComePersons = random.randint(1, int(t)), pPersons=random.randint(1, int(p)))
            self.kasses.append(obj)
            x += 100