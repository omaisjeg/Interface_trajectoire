#!/usr/bin/env python3
# modified version of https://github.com/JonathanPlasse/binary_serial

import serial
import time
from joformat import data2Bytes, bytes2Data, dataSize


class Connection:
    def __init__(self, port='/dev/ttyACM0', baudRate=115200):
        self.ser = serial.Serial(port, baudRate, timeout=1)

    def readData(self, structFormat):
        nbBytes = dataSize(structFormat)
        # Wait until all the data is in the buffer
        while self.ser.in_waiting < nbBytes:
            pass
        # Read the raw data
        rawData = bytearray(nbBytes)
        self.ser.readinto(rawData)
        # Convert the raw data
        data = bytes2Data(structFormat, rawData)
        return data

    def writeData(self, structFormat, data):
        rawData = data2Bytes(structFormat, data)
        self.ser.write(rawData)

    def close(self):
        self.ser.close()
