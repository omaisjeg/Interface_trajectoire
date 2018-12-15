from threading import Thread
import tkinter as Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter.ttk import Frame
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import sleep


class Traj():
    def __init__(self):
        self.t = []
        self.X = []
        self.Y = []
        self.theta = []
        self.coord = [self.t,self.X,self.Y,self.theta]

    def addPoint(self,*arg):
        # arg =  t,x,y,theta
        for q_i in self.coord:
            q_i.append(arg[0])


class Communication(Thread):
    def __init__(self,SerialReference):
        Thread.__init__(self)
        self.serialReference = SerialReference
    def run(self):
        #TODO recuperation des infos du serial
        print("faut mettre des trucs")
    # def sendFactorToMCU(self):
    #     self.serialReference.sendSerialData(self.entry.get() + '%')     # '%' is our ending marker

class Window(Frame):
    def __init__(self, figure, master):
        Frame.__init__(self, master)
        self.entry = None
        self.setPoint = None
        self.master = master        # a reference to the master window
        self.initWindow(figure)     # initialize the window with our settings

    def initWindow(self, figure):
        self.master.title("Real Time Plot")
        canvas = FigureCanvasTkAgg(figure, master=self.master)
        toolbar = NavigationToolbar2Tk(canvas, self.master)
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

       
        lbl1 = Tk.Label(self.master, text="Scaling Factor")
        lbl1.pack(padx=5, pady=5)
        self.entry = Tk.Entry(self.master)
        self.entry.insert(0, '1.0')     # (index, string)
        self.entry.pack(padx=5)
        SendButton = Tk.Button(self.master, text='Send', command=nothing)
        SendButton.pack(padx=5)




print("ok")

def nothing():
    pass

class Fenetre(Thread):
    def __init__(self):
        Thread.__init__(self)


    def run(self):
        print("run")

        fig = plt.figure()

        root = Tk.Tk()
        app = Window(fig, root)
        ax = plt.axes(xlim=(-1,4),ylim=(-1,3))
        ax.grid(True, linestyle='-')
        lines = []

        for i in range(1):
            lines.append(ax.plot([.1,.2,.3], [.1,.3,.8]))

        anim = animation.FuncAnimation(fig, nothing)

        root.mainloop()   # use this instead of plt.show() since we are encapsulating everything in Tkinter
        s.close()

interface = Fenetre()
arduino = Communication(0)

interface.start()
arduino.start()
