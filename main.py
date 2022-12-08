from Queue import *
            
if __name__ == '__main__':
    window = Tk()
    window.title("Queue Visualiztion")
    window.geometry("800x600")
    window.maxsize(1600, 900)
    window.minsize(800, 600)
    gui = Queue(window)
    
    