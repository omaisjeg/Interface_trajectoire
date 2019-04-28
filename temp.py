import socket
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from joformat import Smdata


target = '127.0.0.1'
port = 8653

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((target, port))


x_queue = deque([0]*100, 100)
y_queue = deque([0]*100, 100)
theta_queue = deque([0]*100, 100)

coord = [x_queue, y_queue, theta_queue]


fig, ax = plt.subplots()

lines = ax.plot(np.zeros(100), np.zeros(100), "b",0,0,"rx")
ax.set_title('X/Y Temps réel')
ax.legend()
ax.set_xlim([-.2, 3.2])
ax.set_ylim([-.2, 2.2])


def refresh(i, lines, ax, sock, coordonnees):

    msg = sock.recv(256)
    tmp = Smdata(msg)
    new = tmp.data
    for i in range(3):
        coordonnees[i].append(new[i])

    x_q, y_q, theta_q = coordonnees

    x = np.array(x_q)/100
    y = np.array(y_q)/100
    theta = np.array(theta_q)
    lines[0].set_data(x, y)
    lines[1].set_data(x[-1], y[-1])

    return ax


ani = animation.FuncAnimation(fig, refresh, 100,
                              fargs=(lines, ax, s, coord), interval=30)

plt.show()
