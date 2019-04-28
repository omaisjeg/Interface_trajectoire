import joserial
import maxserver
from joformat import Smdata
from queue import Queue
from threading import Thread


portName = '/dev/ttyACM0'
baudRate = 115200


qsend = Queue()
qrec = Queue()


ard = joserial.Connection(portName, baudRate)
trans = maxserver.Server(8653, qsend, qrec)
trans.start()


def tmpfromard(q, ser):
    while True:
        data = ser.readData('o')
        print(data)
        q.put(data)


def tmptoard(q, ser):
    while True:
        data = q.get()
        print(data)
        if data != "errorconnection":
            ser.writeData(data)


fromar = Thread(target=tmpfromard, args=(qsend, ard))
toard = Thread(target=tmptoard, args=(qrec, ard))

threads = [fromar, toard]

for thr in threads:
    thr.start()

for thr in threads:
    thr.join()


print("fsefd")
