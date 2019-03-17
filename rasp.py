import joserial
import maxserver
from queue import Queue
from threading import Thread


structFormatConfig = ['uint8', 'uint16', 'uint16', 'uint8']
structFormatMeasure = ['uint32', 'uint32', 'float']
portName = '/dev/ttyACM0'
baudRate = 115200


qsend = Queue()
qrec = Queue()


ard = joserial.Connection(portName, baudRate)
trans = maxserver.Server(8456, qsend, qrec)
trans.start()


def tmpfromard(q, ser):
    data = ser.readData(structFormatConfig)
    print(data)
    q.put(data)
    while True:
        data = ser.readData(structFormatMeasure)
        q.put(data)


def tmptoard(q, ser):
    while True:
        data = q.get()
        print(data)
        if data != "errorconnection":
            ser.writeData(structFormatConfig, data)


fromar = Thread(target=tmpfromard, args=(qsend,ard))
toard = Thread(target=tmptoard, args=(qrec,ard))

threads = [fromar, toard]

for thr in threads:
    thr.start()

for thr in threads:
    thr.join()


print("fsefd")
