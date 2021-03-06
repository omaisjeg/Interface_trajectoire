#!/usr/bin/python3
from threading import Thread
from queue import Queue
from time import sleep
from joformat import Smdata
import socket
import numpy as np
import matplotlib.pyplot as plt


target = '127.0.0.1'
port = 8666

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((target, port))


def threadrec(threadname, sock, q):
    # while True:
    #     msg = sock.recv(1024)
    #     data = bytes2Data(structFormatMeasure, msg)
    #     q.put(data)
    #     sleep(0.1)
    timestamps = np.zeros((10, 100))
    positions = np.zeros((10, 100))
    speeds = np.zeros((10, 100))

    msg = sock.recv(256)
    tmp = Smdata(msg)
    print(tmp.info)
    for i in range(10):
        print(i+1, '/', 10)
        for j in range(100):
            msg = sock.recv(256)
            tmp = Smdata(msg)
            timestamps[i, j], positions[i, j], speeds[i, j] = tmp.data
    speed = np.mean(speeds, axis=0)
    t = [i*0.01 for i in range(0, len(speed))]

    plt.plot(t, speed)
    plt.xlabel("Time in seconds")
    plt.ylabel("Speed in steps/seconds")
    plt.show()


def threadsen(threadname, sock, q):
    # while True:
    #     msg = str(q.get())
    #     sock.sendall(msg.encode('UTF-8'))
    #     print(msg)
    msg = Smdata(['c', [10, 100, 1, 220]])
    sock.sendall(msg.bytes)


varshare = Queue()

comenv = Thread(target=threadsen, args=(
    "Communication envoie", s, varshare))
comrec = Thread(target=threadrec, args=(
    "Communication recoie", s, varshare))


threads = [comrec, comenv]

for thr in threads:
    thr.start()

for thr in threads:
    thr.join()
