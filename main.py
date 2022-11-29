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
    
    #Entry settings        
    def kassaParameters(self):
        self.nKassaAmount = Entry(self.window, fg = "black", bg = "white")
        self.nKassaAmount.place(x=65, y=535)
    
    #Function to make kasses
    def setKassa(self, kassaNumber, x, y):
        #init name of kassa
        self.kassaName = Label(self.queue_canvas, text = kassaNumber, fg = "black")
        self.kassaName.place(x = x, y = y)
        
        #draw container
        x2 = x
        y2 = 200
        self.queue_canvas.create_line(x, y, x2, y2, fill="yellow", width=4)
        
        

    #Main function to start queue
    def startQueuesAlgoritm(self):
        kasses = int(self.nKassaAmount.get())
        x = 5
        y = 0
        for kassa in range(kasses):
            self.setKassa(kassa, x, y)
            x += 20
            
if __name__ == '__main__':
    window = Tk()
    window.title("Queue Visualiztion")
    window.geometry("800x600")
    window.maxsize(800, 600)
    window.minsize(800, 600)
    Queue(window)
    window.mainloop()