#!/usr/bin/env python3

from threading import Thread
import tkinter as Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter.ttk import Frame
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from queue import Queue
from time import sleep
import numpy as np
from random import uniform 
import serial
import struct

ser = serial.Serial(port='/dev/ttyACM0',baudrate = 57600,timeout=0.01)

sleep(0.2)
# reçoie 40 octets (10 float32) : odo(temps,x,y,theta) consigne(vg,vd) commande(vg,vd) vitesse(vg,vd)
taillerec = 40
tailleenv = 16
# envoie 16 octets (4 float32) : commande(temps,x,y,theta)


def nothing(rien=0):
    pass

def threadfedtruk(threadname, q, port):
    #read variable "a" modify by thread 2
    print("faut mettre des trucs")
    #TODO recuperation des infos du serial
    t= 0
    while 1:
        sleep(0.1)
        stuff = [[],[]]

        stuff[0].append([t,uniform(0,3),uniform(0,2),uniform(0,360)])
        stuff[1].append([t,uniform(0,3),uniform(0,2),uniform(0,360)])

        q.put(stuff)

        t += 1

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


def threadcomenvoie(threadname, q, port):
    #read variable "a" modify by thread 2

    #TODO recuperation des infos du serial
    t= 0
    while 1:
        if q.qsize() > 10:
            with q.mutex:
                q.queue.clear()
        q.get()

        stuff[0].append([t,uniform(0,3),uniform(0,2),uniform(0,360)])
        stuff[1].append([t,uniform(0,3),uniform(0,2),uniform(0,360)])

        q.put(stuff)

        t += 1
        print("envoie ",t)
        sleep(0.1)



def threadcomrecoie(threadname, q, port):
    #TODO recuperation des infos du serial
    t= 0
    while 1:
        sleep(0.01)

        while port.in_waiting > 9:

            t += 1
            read_serial= ser.read(size=taillerec)
            read = struct.unpack('10f', read_serial)




def threadinter(threadname, q):
    print("run")

    fig = plt.figure()

    root = Tk.Tk()
    app = Window(fig, root)
    ax = plt.axes(xlim=(-1,4),ylim=(-1,3))
    ax.grid(True, linestyle='-')
    lines = []
    newdata = np.array(q.get())
    print(newdata.shape)
    print("blabla")
    for i in range(2):
        lines.append(ax.plot([],[]))

    anim = animation.FuncAnimation(fig, refresh,fargs=(lines, ax, newdata),interval=1000)

    root.mainloop()  




def refresh(frame,lines,ax,newdata):

    for i in range(2):
        lines[i][0].set_xdata(newdata[i,0,1])
        lines[i][0].set_ydata(newdata[i,0,2])
        newdata = lines[i][0].get_xdata(orig=True)
        newdata = lines[i][0].get_ydata(orig=True)
        print(newdata)

varsharefromard = Queue()
varsharetoard = Queue()

comenv = Thread( target=threadcomenvoie, args=("Communication envoie", varsharetoard, ser) )
comrec = Thread( target=threadcomrecoie, args=("Communication recoie", varsharefromard, ser) )
inter = Thread( target=threadinter, args=("Interface", varsharefromard) )
fedtruck = Thread( target=threadinter, args=("Interface", varsharefromard) )

threads = [comenv,comrec,inter,fedtruck]

for thr in threads:
    thr.start()
    thr.join()