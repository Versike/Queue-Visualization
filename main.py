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
        
    #Buttons settings    
    def makeButtons(self):
        self.startQueues = Button(self.window, text = "Start", fg = "Green", command = self.startQueuesAlgoritm)
        self.startQueues.place(x=30, y=535)
        self.pauseQueues = Button(self.window, text = "Stop", fg = "red")
        self.pauseQueues.place(x=130, y=535)
    
    #Entry settings        
    def kassaParameters(self):
        self.nKassaAmount = Entry(self.window, fg = "black", bg = "white", width=5)
        self.nKassaAmount.place(x=65, y=540)
    
    #Function to make kasses
    def setKassa(self, kassaNumber, x, y):
        #init name of kassa
        self.kassaName = Label(self.queue_canvas, text = kassaNumber, fg = "black")
        self.kassaName.place(x = x, y = y)
        
        #draw container
        y2 = 200
        #left line
        self.queue_canvas.create_line(x, y, x, y2, fill="blue", width=4)
        #right line
        xRightOffset = 30
        self.queue_canvas.create_line(x+xRightOffset, y, x+xRightOffset, y2, fill="blue", width=4)
        #upper line
        self.queue_canvas.create_line(x, y2, x+xRightOffset, y2, fill="red", width=4)
        

    #Main function to start queue
    def startQueuesAlgoritm(self):
        kasses = int(self.nKassaAmount.get())
        x = 20
        y = 0
        for kassa in range(kasses):
            self.setKassa(kassa, x, y)
            x += 100
            
if __name__ == '__main__':
    window = Tk()
    window.title("Queue Visualiztion")
    window.geometry("800x600")
    window.maxsize(800, 600)
    window.minsize(800, 600)
    Queue(window)
    window.mainloop()