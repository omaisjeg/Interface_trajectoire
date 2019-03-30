#!/usr/bin/python3
from threading import Thread
from time import sleep
import socket
from joformat import Smdata


class Server(Thread):
    def __init__(self, port, sendqueue, receivequeue):
        Thread.__init__(self)
        self.port = port
        self.sq = sendqueue
        self.rq = receivequeue

    def run(self):

        # create a socket object
        serversocket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)

        # bind to the port
        serversocket.bind(('', self.port))

        # queue up to 5 requests
        serversocket.listen(2)
        clientsocket, addr = serversocket.accept()
        print("Got a connection from %s" % str(addr))

        def threadrec(threadname, sock, q):

            while True:
                try:
                    msg = sock.recv(256)
                except:
                    q.put("errorconnection")
                    break
                tmp = Smdata(msg)
                q.put(tmp.info)

        def threadsen(threadname, sock, q):
            while True:
                try:
                    tmp = q.get()
                except:
                    break
                msg = Smdata(tmp)
                sock.sendall(msg.bytes)

        comenv = Thread(target=threadsen, args=(
            "Communication envoie", clientsocket, self.sq))
        comrec = Thread(target=threadrec, args=(
            "Communication recoie", clientsocket, self.rq))

        self.threads = [comrec, comenv]

        for thr in self.threads:
            thr.start()

        for thr in self.threads:
            thr.join()


if __name__ == '__main__':
    port = 8456
    a = Server(port)
    while True:
        a.start()
