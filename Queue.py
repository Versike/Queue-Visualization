from tkinter import *
from random import randint, choice
from Kassa import *
import asyncio
import itertools
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
        self.personarr = 0
        
        #Canvas settings
        self.canvasWidth = 700
        self.canvasHeight = 500
        
        self.emptyQueueCanvas = Canvas(self.window, width=self.canvasWidth, height=self.canvasHeight,bg="white", relief=RAISED, bd=10)
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
        self.startQueues = Button(self.window, text = "Start", fg = "Green", command = async_handler(self.initKasses))
        self.startQueues.place(x=30, y=535)
        
        self.pauseQueues = Button(self.window, text = "Stop", fg = "red", command = async_handler(self.ebalYaVRot))
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
    async def initKasses(self):
        kassaAmount = int(self.nKassaAmount.get())
        x = 20
        y = 0
        self.kasses = []
        self.kassesLabels = []
        
        for kassaNumber in range(kassaAmount):
            kassa = Kassa()
            kassa.number = kassaNumber
            kassa.x = x
            kassa.y = y
            self.kasses.append(kassa)
            self.drawKassa(kassa.number, x , y)
            label = Label(self.queue_canvas, text = 0, fg = "black")
            self.kassesLabels.append(label)
            x += 100
        print(f'[+] Initialize kasses')
        asyncio.ensure_future(self.updatekasess())
        print(f'[+] Start arrival peoples to Kasses by findMin()')

    async def updatekasess(self):
        while True:
            delay = randint(1, int(self.tTimeComePersons.get()))
            self.personarr = randint(1, int(self.pPersons.get()))
            self.arrivalPersons["text"] = self.personarr
            await asyncio.sleep(delay)
            for i in range(self.personarr):
                kassa = self.findMin()
                kassa.queue.append(i)
                self.kassesLabels[kassa.number]["text"] = str(len(kassa.queue))
                self.kassesLabels[kassa.number].place(x = kassa.x, y = kassa.y + 20)
                print(f'Касса {str(kassa.number)} имеет очередь {str(len(kassa.queue))}')
                await asyncio.sleep(0.01)
            self.personarr = 0

    async def servePeople(self, numberKassa):
        kassa = self.kasses
        delay = randint(1, 3)
        print(f'[+] Serving peoples')
        while True:
            if kassa[numberKassa].queue and self.personarr > 0:
                kassa[numberKassa].queue.pop(0)
                self.kassesLabels[numberKassa]["text"] = str(len(kassa[numberKassa].queue))
                print(f'Касса {kassa[numberKassa].number} обслужила. В очереди {len(kassa[numberKassa].queue)}')
            await asyncio.sleep(delay)
    
    def findMin(self): # return class Kassa
        r = self.kasses[0]
        for i in self.kasses[1:]:
            if len(i.queue) < len(r.queue):
                r = i
            if(len(i.queue)==len(r.queue) and len(i.queue) == 0):
                r=choice([i, r])
        return r
        
    async def ebalYaVRot(self):
        kassaAmount = int(self.nKassaAmount.get())
        for kassaNumber in range(kassaAmount):
            asyncio.ensure_future(self.servePeople(kassaNumber))