from tkinter import *
from random import randint
from Kassa import *
import asyncio
from async_tkinter_loop import async_handler, async_mainloop
from defines import *

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
        
        async_mainloop(self.window)
        
    #Labels for entry's elements
    def entryLabels(self):
        self.kassaAmount = Label(self.window, text = "N", fg = "black")
        self.kassaAmount.place(x=140, y=538)
        
        self.timeComePersons = Label(self.window, text = "T", fg = "black")
        self.timeComePersons.place(x=180, y=538)
        
        self.Persons = Label(self.window, text = "P", fg = "black")
        self.Persons.place(x=220, y=538)
        
        self.arrivalPersons = Label(self.window, text = text_arrival_persons, fg = "black")
        self.arrivalPersons.place(x=300, y = 538)
        
    #Buttons settings    
    def makeButtons(self):
        self.startQueues = Button(self.window, text = "Start", fg = "Green", command = async_handler(self.arrPer))
        self.startQueues.place(x=30, y=535)
        
        self.pauseQueues = Button(self.window, text = "Stop", fg = "red", command = async_handler(self.minusPer))
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
        self.labelPersons = []
        self.labelTimer = []
        self.kasses = []
        for kassaNumber in range(kassaAmount):
            kassa = Kassa()
            kassa.number = kassaNumber
            self._lPersons = Label(self.queue_canvas, text = str(len(kassa.queue)))
            self.labelPersons.append(self._lPersons)
            self.kasses.append(kassa)
            x += 100
    
    async def arrPer(self): # delay done
        while True:
            delay = randint(1, int(self.tTimeComePersons.get()))
            personarr = randint(1, int(self.pPersons.get()))
            self.arrivalPersons["text"] = text_arrival_persons + str(self.QueuePersons)
            self.QueuePersons += personarr
            await asyncio.sleep(delay)
    
    async def minusPer(self):
        var = int(self.QueuePersons - 3)
        self.QueuePersons = var
        
    