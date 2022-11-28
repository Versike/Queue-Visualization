from tkinter import *
import time

class Queue:
    def __init__(self, root):
        self.window = root
        self.window.config(bg="white")
        
        #Elements initialization
        self.kassaName = None
        self.startQueues = None
        self.nKassaAmount = None
        
        #Canvas settings
        self.canvasWidth = 700
        self.canvasHeight = 500
        
        self.queue_canvas = Canvas(self.window, width=self.canvasWidth, height=self.canvasHeight,bg="white", relief=RAISED, bd=10)
        self.queue_canvas.pack(fill=BOTH)
        
        #Call functions
        self.makeButtons()
        self.kassaParameters()
    
    def setKassa(self, kassaNumber, x, y):
        self.kassaName = Label(self.queue_canvas, text = kassaNumber, fg = "black")
        self.kassaName.place(x = x, y = y)
        
    def makeButtons(self):
        self.startQueues = Button(self.window, text = "Start", fg = "Green", command = self.startQueuesAlgoritm)
        self.startQueues.place(x=30, y=535)
        
    def startQueuesAlgoritm(self):
        kasses = int(self.nKassaAmount.get())
        x = 0
        y = 0
        for kassa in range(kasses):
            self.setKassa(kassa, x, y)
            x += 20
            
        
    def kassaParameters(self):
        self.nKassaAmount = Entry(self.window, fg = "black", bg = "white")
        self.nKassaAmount.place(x=65, y=535)

if __name__ == '__main__':
    window = Tk()
    window.title("Queue Visualiztion")
    window.geometry("800x600")
    window.maxsize(800, 600)
    window.minsize(800, 600)
    Queue(window)
    window.mainloop()