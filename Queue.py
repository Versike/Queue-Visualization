from tkinter import *
from random import randint, choice, uniform
from Kassa import *
import asyncio
import numpy as np
from async_tkinter_loop import async_handler, async_mainloop
from defines import *


class Queue(Frame):
    def __init__(self, root):
        super().__init__()
        self.window = root
        self.window.config(bg="white")

        # boolean
        self.checkOfFirstRun = False

        # lists
        self.kasses = []

        # Elements initialization
        self.kassaName = None
        self.startQueues = None
        self.nKassaAmount = None

        # Parameters
        self.QueuePersons = 0
        self.personarr = 0
        self.servePeopleMean = 0
        self.kassaAmount = 0
        self.lastXOfKassa = 0
        self.y = 10
        self.lastAmount = 0

        # Canvas settings
        self.canvasWidth = 700
        self.canvasHeight = 500

        self.queue_canvas = Canvas(self.window, width=self.canvasWidth, height=self.canvasHeight, bg="white", bd=10)
        self.empty_queue_canvas = Canvas(self.window, width=self.canvasWidth, height=self.canvasHeight, bg="white",
                                         bd=10)
        self.queue_canvas.config(scrollregion=self.queue_canvas.bbox("all"))
        self.queue_canvas.pack(expand=YES, fill=BOTH)

        # Scrollbar

        # Call functions
        self.entryLabels()
        self.makeButtons()
        self.kassaParameters()

        self.scrollX = Scrollbar(self.queue_canvas)
        self.scrollX.pack(side=BOTTOM, fill=X)

        self.queue_canvas.config(xscrollcommand=self.scrollX.set)
        self.scrollX.config(command=self.queue_canvas.xview)

        async_mainloop(self.window)

    # Labels for entry's elements
    def entryLabels(self):
        self.kassaAmount = Label(self.window, text="N", fg="black")
        self.kassaAmount.place(x=140, y=538)

        self.timeComePersons = Label(self.window, text="T", fg="black")
        self.timeComePersons.place(x=180, y=538)

        self.Persons = Label(self.window, text="P", fg="black")
        self.Persons.place(x=220, y=538)

        self.arrivalPersons = Label(self.window, text=text_arrival_persons, fg="black")
        self.arrivalPersons.place(x=300, y=538)

    # Buttons settings
    def makeButtons(self):
        self.startQueues = Button(self.window, text="Start", fg="Green", command=async_handler(self.checkToStart))
        self.startQueues.place(x=30, y=535)

        self.pauseQueues = Button(self.window, text="Stop", fg="red", command=async_handler(self.pauseProgram))
        self.pauseQueues.place(x=70, y=535)

    # Entry settings
    def kassaParameters(self):
        self.reg = self.register(self.callback)
        self.nKassaAmount = Entry(self.window, fg="black", bg="white", width=2)
        self.nKassaAmount.place(x=150, y=540)
        self.nKassaAmount.config(validate="key", validatecommand=(self.reg, '%P'))

        self.tTimeComePersons = Entry(self.window, fg="black", bg="white", width=2)
        self.tTimeComePersons.place(x=190, y=540)
        self.tTimeComePersons.config(validate="key", validatecommand=(self.reg, '%P'))

        self.pPersons = Entry(self.window, fg="black", bg="white", width=2)
        self.pPersons.place(x=230, y=540)
        self.pPersons.config(validate="key", validatecommand=(self.reg, '%P'))

    def callback(self, value):

        if value.isdigit():
            return True
        elif value == "":
            return True
        else:
            return False

    # Function to make kasses
    def drawKassa(self, kassaNumber, x, y, tck1, tck2):
        # init name of kassa
        self.kassaName = Label(self.queue_canvas, text="?????????? " + str(kassaNumber), fg="black")
        self.queue_canvas.create_window(x, y, window=self.kassaName)
        self.kassaQueuePersons = Label(self.queue_canvas, text=self.QueuePersons, fg="black")
        self.queue_canvas.create_window(x, y + 20, window=self.kassaQueuePersons)
        self.serveMean = Label(self.queue_canvas, text=self.servePeopleMean, fg="black")
        self.queue_canvas.create_window(x, y + 40, window=self.serveMean)
        self.statuskassa = Label(self.queue_canvas, text="status", fg="black")
        self.queue_canvas.create_window(x, y + 60, window=self.statuskassa)
        self.tck1 = Entry(self.window, fg="black", bg="white", width=2, textvariable=tck1)
        self.queue_canvas.create_window(x, y + 80, window=self.tck1)
        self.tck2 = Entry(self.window, fg="black", bg="white", width=2, textvariable=tck2)
        self.queue_canvas.create_window(x, y + 100, window=self.tck2)
        self.tck2.config(validate="key", validatecommand=(self.reg, '%P'))

    # Main function to start queue
    async def initKasses(self):
        self.kassaAmount = int(self.nKassaAmount.get())
        x = 20
        self.kasses = []
        self.kassesNameLabels = []
        self.kassesLabels = []
        self.kassesMean = []
        self.kassesStatus = []
        self.kassesTck1 = []
        self.kassesTck2 = []
        for kassaNumber in range(len(self.kasses), self.kassaAmount):
            kassa = Kassa()
            kassa.number = kassaNumber
            kassa.x = x
            kassa.y = self.y
            self.kasses.append(kassa)
            self.drawKassa(kassa.number, kassa.x, kassa.y, kassa.tck1, kassa.tck2)
            nameLabel = Label(self.queue_canvas, text=f'?????????? {kassa.number}', fg="black")
            self.kassesNameLabels.append(nameLabel)
            label = Label(self.queue_canvas, text=0, fg="black")
            self.kassesLabels.append(label)
            mean = Label(self.queue_canvas, text=0, fg="black")
            self.kassesMean.append(mean)
            status = Label(self.queue_canvas, text="status", fg="black")
            self.kassesStatus.append(status)
            tck1 = Entry(self.window, fg="black", bg="white", width=2, textvariable=kassa.tck1)
            self.kassesTck1.append(tck1)
            tck2 = Entry(self.window, fg="black", bg="white", width=2, textvariable=kassa.tck2)
            self.kassesTck2.append(tck2)
            self.lastXOfKassa = kassa.x
            x += 100
        # print(f'[+] Initialize kasses')
        self.task_update = asyncio.ensure_future(self.updatekasess())
        self.task_stastus = asyncio.ensure_future(self.statusKasses())
        # print(f'[+] Start arrival peoples to Kasses by findMin()')
        if self.checkOfFirstRun is False:
            self.task_serving = asyncio.ensure_future(self.loopServing())

    async def addKasses(self):
        x = self.lastXOfKassa + 100
        y = 0
        self.kassaAmount = int(self.nKassaAmount.get())
        for kassa in range(len(self.kasses), self.kassaAmount):
            kas = Kassa()
            kas.number = kassa
            kas.x = x
            kas.y = self.y
            self.drawKassa(kas.number, kas.x, kas.y, kas.tck1, kas.tck2)
            self.kasses.append(kas)
            label = Label(self.queue_canvas, text=0, fg="black")
            self.kassesLabels.append(label)
            mean = Label(self.queue_canvas, text=0, fg="black")
            self.kassesMean.append(mean)
            status = Label(self.queue_canvas, text="status", fg="black")
            self.kassesStatus.append(status)
            nameLabel = Label(self.queue_canvas, text=f'?????????? {kas.number}', fg="black")
            self.kassesNameLabels.append(nameLabel)
            tck1 = Entry(self.window, fg="black", bg="white", width=2, textvariable=kas.tck1)
            self.kassesTck1.append(tck1)
            tck2 = Entry(self.window, fg="black", bg="white", width=2, textvariable=kas.tck2)
            self.kassesTck2.append(tck2)
            self.lastXOfKassa = kas.x
            x += 100

    async def updatekasess(self):
        while True:
            if self.tTimeComePersons.get() == '':
                time_pc = 5
            else:
                time_pc = int(self.tTimeComePersons.get())
            if self.pPersons.get() == '':
                p_count = 3
            else:
                p_count = int(self.pPersons.get())
            delay = randint(1, time_pc)
            self.personarr = randint(1, p_count)
            self.arrivalPersons["text"] = self.personarr
            await asyncio.sleep(delay)
            for i in range(self.personarr):
                kassa = self.findMin()
                kassa.queue.append(i)
                self.kassesLabels[kassa.number]["text"] = str(len(kassa.queue))
                # print(f'?????????? {str(kassa.number)} ?????????? ?????????????? {str(len(kassa.queue))}')
                await asyncio.sleep(0.01)
            self.personarr = 0

    async def statusKasses(self):
        while True:
            mx = max(self.kasses, key=lambda el: len(el.queue))
            mn = min(self.kasses, key=lambda el: len(el.queue))
            for i in self.kasses:
                q_length = len(i.queue)
                if q_length == len(mx.queue):
                    self.kassesStatus[i.number]["text"] = "*Busy*"
                elif q_length == len(mn.queue) or q_length == 0:
                    self.kassesStatus[i.number]["text"] = "_Free_"
                else:
                    self.kassesStatus[i.number]["text"] = "_____"

                self.queue_canvas.create_window(i.x, i.y + 60, window=self.kassesStatus[i.number])

            await asyncio.sleep(0.1)

    async def servePeople(self, numberKassa):
        kassa = self.kasses
        # print(f'[+] Serving peoples {self.kassesTck2[numberKassa].get()}')
        while True:
            # print(f'[servePeople] {numberKassa}')
            if kassa[numberKassa].queue:
                if self.kassesTck1[numberKassa].get() == '' or self.kassesTck2[numberKassa].get() == '':
                    tck1 = 3
                    tck2 = 7
                else:
                    tck1 = int(self.kassesTck1[numberKassa].get())
                    tck2 = int(self.kassesTck2[numberKassa].get())
                delay = uniform(tck1, tck2)
                # print(f'[servePeople] {delay} ??????????????')
                kassa[numberKassa].countOfDelay += 1
                kassa[numberKassa].delay.append(delay)
                kassa[numberKassa].mean = round(np.sum(kassa[numberKassa].delay) / kassa[numberKassa].countOfDelay, 2)
                kassa[numberKassa].queue.pop(0)
                self.kassesMean[numberKassa]["text"] = str(kassa[numberKassa].mean)
                self.queue_canvas.create_window(kassa[numberKassa].x, kassa[numberKassa].y + 40,
                                                window=self.kassesMean[numberKassa])
                self.kassesLabels[numberKassa]["text"] = str(len(kassa[numberKassa].queue))
                self.queue_canvas.create_window(kassa[numberKassa].x, kassa[numberKassa].y + 20,
                                                window=self.kassesLabels[numberKassa])
                # print(f'?????????? {kassa[numberKassa].number} ??????????????????. ?? ?????????????? {len(kassa[numberKassa].queue)}')
                await asyncio.sleep(delay)
            await asyncio.sleep(0.01)

    def findMin(self):  # return class Kassa
        r = self.kasses[0]
        for i in self.kasses[1:]:
            if len(i.queue) < len(r.queue):
                r = i
            elif len(i.queue) == len(r.queue) or len(i.queue) == 0:
                r = choice([i, r])
        return r

    # For find busy kassa   
    def findMax(self):
        r = self.kasses[0]
        for i in self.kasses[1:]:
            if len(i.queue) > len(r.queue):
                r = i
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
        self.task_stastus.cancel()
        self.kassaQueuePersons.master.destroy
        # print(f'[LOG] pauseProgram.self.kasses = {len(self.kasses)}')
        for kassa in range(self.kassaAmount):
            # print(f'[LOG] ?????????????????????? ?????????? {kassa}')
            self.listOfTasksByKassa[kassa].cancel()

    # ?????? ?????????????? ?????????????????? ???????????????? ?????? ???????????????? ?????? ?????? ???????????????????? ?? ?????????????????? ???? ????????.
    # ???????? ???????????????? ???? ???????????? ???????? ?? ?????????????????????? ??????????. ?? ?????????? ???????????? ??????????????
    async def resumeProgram(self):
        self.kassaAmount = int(self.nKassaAmount.get())
        temp = len(self.kasses)
        # print(f'[LOG] temp: {temp} and kassaAmount: {self.kassaAmount}')
        if temp > self.kassaAmount:
            await self.pauseProgram()
            self.kassaAmount = int(self.nKassaAmount.get())
            # print(f'[LOG] ?????????? ?? IF')
            peopleOutKassa = []
            self.queue_canvas.delete("all")
            for kassa in range(self.kassaAmount, temp):
                peopleOutKassa += self.kasses[-1].queue
                self.kasses.pop()
                self.kassesLabels.pop()
                self.kassesMean.pop()
                self.listOfTasksByKassa.pop()
                self.kassesNameLabels.pop()
                self.kassesTck1.pop()
                self.kassesTck2.pop()
                self.lastXOfKassa = self.kasses[len(self.kasses) - 1].x

                print(f'[-] ?????????? {kassa} ???????? ??????????????. ?????????? ?????? ???????????????????? ?? ??/?? 15?? ?? ??????.')
                # temp = len(self.kasses)
            for i in peopleOutKassa:
                print(f'[-] ?????????????????????? ??????????????. {i}')
                self.findMin().queue.append(i)
            self.task_update = asyncio.ensure_future(self.updatekasess())
            self.task_stastus = asyncio.ensure_future(self.statusKasses())
            for kassa in range(len(self.kasses)):
                # print(f'[LOG] ?????????? {self.kasses[kassa].number} ?????????????? {len(self.kasses[kassa].queue)}')
                self.queue_canvas.create_window(self.kasses[kassa].x, self.kasses[kassa].y,
                                                window=self.kassesNameLabels[self.kasses[kassa].number])
                self.kassesLabels[self.kasses[kassa].number]["text"] = str(len(self.kasses[kassa].queue))
                self.queue_canvas.create_window(self.kasses[kassa].x, self.kasses[kassa].y + 20,
                                                window=self.kassesLabels[self.kasses[kassa].number])
                self.queue_canvas.create_window(self.kasses[kassa].x, self.kasses[kassa].y + 80,
                                                window=self.kassesTck1[self.kasses[kassa].number])
                self.queue_canvas.create_window(self.kasses[kassa].x, self.kasses[kassa].y + 100,
                                                window=self.kassesTck2[self.kasses[kassa].number])
                self.listOfTasksByKassa[kassa] = asyncio.ensure_future(self.servePeople(kassa))
            # print(f'[resumeProgram] ???????? {len(self.kasses)} ?????????? {len(self.listOfTasksByKassa)}')

        if temp < self.kassaAmount:
            await self.addKasses()
            self.task_update = asyncio.ensure_future(self.updatekasess())
            self.task_stastus = asyncio.ensure_future(self.statusKasses())
            for kassa in range(temp, self.kassaAmount):
                # print(f'[+] ?????????? {kassa} ???????? ??????????????????.')
                self.listOfTasksByKassa.append(asyncio.ensure_future(self.servePeople(kassa)))

        elif temp == self.kassaAmount:
            self.kassaAmount = int(self.nKassaAmount.get()) - 1
            await self.pauseProgram()
            self.task_update = asyncio.ensure_future(self.updatekasess())
            self.task_stastus = asyncio.ensure_future(self.statusKasses())
            for kassa in range(self.kassaAmount):
                self.listOfTasksByKassa[kassa] = asyncio.ensure_future(self.servePeople(kassa))

    async def checkToStart(self):
        if len(self.kasses) > 0:
            self.checkOfFirstRun = True
            await self.resumeProgram()
            # print("[+] ???????????????? ????????????")
        else:
            await self.initKasses()
