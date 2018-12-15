from threading import Thread
import tkinter as Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter.ttk import Frame
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import sleep


from random import uniform # pour tester le code 

class Traj():
    def __init__(self):
        self.t = []
        self.X = []
        self.Y = []
        self.theta = []
        self.coord = [self.t,self.X,self.Y,self.theta]

    def addPoint(self,arg):
        # arg =  t,x,y,theta
        for i in range(len(arg)):
            self.coord[i].append(arg[i])


class Communication(Thread):
    def __init__(self,SerialReference):
        Thread.__init__(self)
        self.serialReference = SerialReference
        self.t = 0
    def run(self):


        print("faut mettre des trucs")
        #TODO recuperation des infos du serial
        

        while 1:
            sleep(0.1)
            trajs[0].addPoint([self.t,uniform(0,3),uniform(0,2),uniform(0,360)])
            trajs[1].addPoint([self.t,uniform(0,3),uniform(0,2),uniform(0,360)])

            self.t += 1


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

def nothing(rien=0):
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

        for i in range(2):
            lines.append(ax.plot(trajs[i].X, trajs[i].Y))

        anim = animation.FuncAnimation(fig, self.refresh,fargs=(lines, ax),interval=100)

        root.mainloop()   # use this instead of plt.show() since we are encapsulating everything in Tkinter
        s.close()
    def refresh(self,frame,lines,ax):
        for i in range(2):
            lines.append(ax.plot(trajs[i].X, trajs[i].Y))


testodoTraj, testcommandTraj = Traj(),Traj()
trajs = [testodoTraj, testcommandTraj]

interface = Fenetre()
arduino = Communication(0)


arduino.start()
interface.start()
