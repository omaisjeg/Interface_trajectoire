import joserial
import maxserver
from joformat import structFormatConfig, structFormatMeasure, bytes2Data, Smdata
from queue import Queue
from threading import Thread


portName = '/dev/ttyACM0'
baudRate = 115200


qsend = Queue()
qrec = Queue()


ard = joserial.Connection(portName, baudRate)
trans = maxserver.Server(8766, qsend, qrec)
trans.start()


def tmpfromard(q, ser):
    rawData = ser.readData()
    data = bytes2Data(structFormatConfig, rawData)
    q.put(['c', data])
    while True:
        rawData = ser.readData()
        data = bytes2Data(structFormatMeasure, rawData)
        q.put(['m', data])


def tmptoard(q, ser):
    while True:
        data = q.get()
        print(data)
        if data != "errorconnection":
            info = Smdata(data)
            ser.writeData(info.bytes)


fromar = Thread(target=tmpfromard, args=(qsend, ard))
toard = Thread(target=tmptoard, args=(qrec, ard))

threads = [fromar, toard]

for thr in threads:
    thr.start()

for thr in threads:
    thr.join()


print("fsefd")
