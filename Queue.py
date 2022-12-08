from tkinter import *
from random import randint, choice, uniform
from Kassa import *
import asyncio
import numpy as np
from async_tkinter_loop import async_handler, async_mainloop
from defines import *

class Queue:
    def __init__(self, root):
        self.window = root
        self.window.config(bg="white")
        
        #boolean
        self.checkOfFirstRun = False
        
        #lists
        self.kasses = []
        
        #Elements initialization
        self.kassaName = None
        self.startQueues = None
        self.nKassaAmount = None
        
        #Parameters
        self.QueuePersons = 0
        self.personarr = 0
        self.servePeopleMean = 0
        self.kassaAmount = 0
        self.lastXOfKassa = 0
        
        #Canvas settings
        self.canvasWidth = 700
        self.canvasHeight = 500
        
        self.queue_canvas = Canvas(self.window, width=self.canvasWidth, height=self.canvasHeight,bg="white", bd=10)
        self.queue_canvas.config(scrollregion=self.queue_canvas.bbox("all"))
        self.queue_canvas.pack(expand=YES, fill=BOTH)
        
        #Scrollbar
        
        #Call functions
        self.entryLabels()
        self.makeButtons()
        self.kassaParameters()
        
        self.scrollX = Scrollbar(self.queue_canvas)
        self.scrollX.pack(side=BOTTOM, fill=X)
        
        self.queue_canvas.config(xscrollcommand=self.scrollX.set)
        self.scrollX.config(command=self.queue_canvas.xview)
        
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
        self.startQueues = Button(self.window, text = "Start", fg = "Green", command = async_handler(self.checkToStart))
        self.startQueues.place(x=30, y=535)
        
        self.pauseQueues = Button(self.window, text = "Stop", fg = "red", command = async_handler(self.pauseProgram))
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
        self.serveMean = Label(self.queue_canvas, text = self.servePeopleMean, fg = "black")
        self.serveMean.place(x=x, y=y+40)
        self.statuskassa = Label(self.queue_canvas, text = "status", fg = "black")
        self.statuskassa.place(x=x, y=y+60)
        
    #Main function to start queue
    async def initKasses(self):
        self.kassaAmount = int(self.nKassaAmount.get())
        x = 20
        y = 0
        self.kasses = []
        self.kassesLabels = []
        self.kassesMean = []
        self.kassesStatus = []
        
        for kassaNumber in range(len(self.kasses), self.kassaAmount):
            kassa = Kassa()
            kassa.number = kassaNumber
            kassa.x = x
            kassa.y = y
            self.kasses.append(kassa)
            self.drawKassa(kassa.number, x , y)
            label = Label(self.queue_canvas, text = 0, fg = "black")
            self.kassesLabels.append(label)
            mean = Label(self.queue_canvas, text = 0, fg = "black")
            self.kassesMean.append(mean)
            status = Label(self.queue_canvas, text = "status", fg = "black")
            self.kassesStatus.append(status)
            self.lastXOfKassa = kassa.x
            x += 100
        print(f'[+] Initialize kasses')
        self.task_update = asyncio.ensure_future(self.updatekasess())
        print(f'[+] Start arrival peoples to Kasses by findMin()')
        if self.checkOfFirstRun is False:
            self.task_serving = asyncio.ensure_future(self.loopServing())
            
    async def addKasses(self):
        x = self.lastXOfKassa + 100
        y = 0
        self.kassaAmount = int(self.nKassaAmount.get())
        for kassa in range(len(self.kasses),self.kassaAmount):
            kas = Kassa()
            kas.number = kassa
            kas.x = x
            kas.y = y 
            self.drawKassa(kas.number, x , y)
            self.kasses.append(kas)
            label = Label(self.queue_canvas, text = 0, fg = "black")
            self.kassesLabels.append(label)
            mean = Label(self.queue_canvas, text = 0, fg = "black")
            self.kassesMean.append(mean)
            status = Label(self.queue_canvas, text = "status", fg = "black")
            self.kassesStatus.append(status)
            self.lastXOfKassa = kas.x
            x += 100

    async def updatekasess(self):
        while True:
            delay = randint(1, int(self.tTimeComePersons.get()))
            self.personarr = randint(1, int(self.pPersons.get()))
            self.arrivalPersons["text"] = self.personarr
            await asyncio.sleep(delay)
            for i in range(self.personarr):
                kassa = await self.findMin()
                kassa2 = await self.findMax()
                kassa.queue.append(i)
                self.kassesStatus[kassa.number]["text"] = "_Free_"
                self.kassesStatus[kassa.number].place(x=kassa.x, y = kassa.y + 60)
                self.kassesStatus[kassa2.number]["text"] = "_Busy_"
                self.kassesStatus[kassa2.number].place(x=kassa.x, y = kassa.y + 60)
                self.kassesLabels[kassa.number]["text"] = str(len(kassa.queue))
                self.kassesLabels[kassa.number].place(x = kassa.x, y = kassa.y + 20)
                print(f'Касса {str(kassa.number)} имеет очередь {str(len(kassa.queue))}')
                await asyncio.sleep(0.01)
            self.personarr = 0

    async def servePeople(self, numberKassa):
        kassa = self.kasses
        print(f'[+] Serving peoples')
        while True:
            print(f'[servePeople] {numberKassa}')
            if kassa[numberKassa].queue and self.personarr > 0:
                delay = uniform(1, 8)
                kassa[numberKassa].countOfDelay += 1
                kassa[numberKassa].delay.append(delay)
                kassa[numberKassa].mean = round(np.sum(kassa[numberKassa].delay)/kassa[numberKassa].countOfDelay, 2)
                kassa[numberKassa].queue.pop(0)
                self.kassesMean[numberKassa]["text"] = str(kassa[numberKassa].mean)
                self.kassesMean[numberKassa].place(x=kassa[numberKassa].x, y=kassa[numberKassa].y + 40)
                self.kassesLabels[numberKassa]["text"] = str(len(kassa[numberKassa].queue))
                self.kassesLabels[numberKassa].place(x=kassa[numberKassa].x, y=kassa[numberKassa].y + 20)
                print(f'Касса {kassa[numberKassa].number} обслужила. В очереди {len(kassa[numberKassa].queue)}')
                await asyncio.sleep(delay)
            await asyncio.sleep(0.01)
    
    async def findMin(self): # return class Kassa
        r = self.kasses[0]
        for i in self.kasses[1:]:
            if len(i.queue) < len(r.queue):
                r = i
            if len(i.queue)==len(r.queue) or len(i.queue) == 0:
                r=choice([i, r])
        await asyncio.sleep(0.1)
        return r
        
    # For find busy kassa   
    async def findMax(self):
        r = self.kasses[0]
        for i in self.kasses[1:]:
            if len(i.queue) > len(r.queue):
                r = i
        await asyncio.sleep(0.1)
        return r
        
    async def loopServing(self):
        self.kassaAmount = int(self.nKassaAmount.get())
        self.listOfTasksByKassa = []
        if self.checkOfFirstRun is False:
            for kassaNumber in range(self.kassaAmount):
                self.listOfTasksByKassa.append(asyncio.ensure_future(self.servePeople(kassaNumber)))
    
    async def pauseProgram(self):
        self.kassaAmount = int(self.nKassaAmount.get())
        self.task_update.cancel()
        self.kassaQueuePersons.master.destroy
        print(f'[LOG] pauseProgram.self.kasses = {len(self.kasses)}')
        for kassa in range(self.kassaAmount):
            print(f'[LOG] Останвливаю кассу {kassa}')
            self.listOfTasksByKassa[kassa].cancel()        
        
    #ТУТ БОЛЬШАЯ СТРАШИЛКА ЗАПРЕЩАЮ ВАМ СМОТРЕТЬ ЧТО ТУТ ПРОИСХОДИТ Я ОБЪЯСНЯТЬ НЕ БУДУ. КУЧА ПРОВЕРОК НА КАЖДЫЙ ТАСК И АСИНХРОННЫЙ ВЫЗОВ. Я ЛУЧШЕ ВЫКИНУ ЗАЧЕТКУ
    async def resumeProgram(self):
        self.kassaAmount = int(self.nKassaAmount.get())
        temp = len(self.kasses)
        print(f'[LOG] temp: {temp} and kassaAmount: {self.kassaAmount}')
        if temp > self.kassaAmount:
            await self.pauseProgram()
            print(f'[LOG] Зашел в IF')
            peopleOutKassa = 0
            for kassa in range(self.kassaAmount, temp):
                peopleOutKassa += len(self.kasses[temp-1].queue)
                self.kassesLabels[kassa]["text"] = "-rm"
                self.kassesLabels[kassa].place(x=self.kasses[kassa].x, y=20)
                self.kassesMean[kassa]["text"] = "-rm"
                self.kassesMean[kassa].place(x=self.kasses[kassa].x, y=40)
                self.kassesStatus[kassa]["text"] = "-rm"
                self.kassesStatus[kassa].place(x=self.kasses[kassa].x, y=60)
                self.kasses.pop(temp-1)
                self.kassesLabels.pop(temp-1)
                self.kassesMean.pop(temp-1)
                self.listOfTasksByKassa.pop(temp-1)
                self.lastXOfKassa = self.kasses[len(self.kasses)-1].x
                
                print(f'[-] Касса {kassa} была удалена. Удачи вам помучаться с з/п 15к в мес.')
                temp -= 1
            for i in range(peopleOutKassa):
                self.findMin().queue.append(i)
            self.task_update = asyncio.ensure_future(self.updatekasess())
            for kassa in range(len(self.kasses)):
                print(f'[LOG] Касса {self.kasses[kassa].number} очередь {len(self.kasses[kassa].queue)}')
                self.listOfTasksByKassa[kassa] = asyncio.ensure_future(self.servePeople(kassa))
            print(f'[resumeProgram] Касс {len(self.kasses)} Таски {len(self.listOfTasksByKassa)}')
            
        if temp < self.kassaAmount:
            await self.addKasses()
            self.task_update = asyncio.ensure_future(self.updatekasess())
            print('asd')
            for kassa in range(temp, self.kassaAmount):
                print(f'[+] Касса {kassa} была добавлена.')
                self.listOfTasksByKassa.append(asyncio.ensure_future(self.servePeople(kassa)))
                
        elif temp == self.kassaAmount:
            self.kassaAmount = int(self.nKassaAmount.get()) - 1
            await self.pauseProgram()
            self.task_update = asyncio.ensure_future(self.updatekasess())
            for kassa in range(self.kassaAmount):
                self.listOfTasksByKassa[kassa] = asyncio.ensure_future(self.servePeople(kassa))
                
    async def checkToStart(self):
        if len(self.kasses) > 0:
            self.checkOfFirstRun = True
            await self.resumeProgram()
            print("[+] ВРУБАЙСЯ БРАТАН")
        else:
            await self.initKasses()
    
    