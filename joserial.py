#!/usr/bin/env python3
# modified version of https://github.com/JonathanPlasse/binary_serial

import serial
import time
from joformat import dataSize, formatDict, Smdata


class Connection:
    def __init__(self, port='/dev/ttyACM0', baudRate=115200):
        self.ser = serial.Serial(port, baudRate, timeout=1)

    def readData(self):
        while self.ser.in_waiting < 3:
            pass
        header = bytearray(3)
        self.ser.readinto(header)
        name = header[1:2].decode('ASCII')
        nbBytes = dataSize(formatDict[name])
        # Wait until all the data is in the buffer
        while self.ser.in_waiting < nbBytes:
            pass
        # Read the raw data
        rawData = bytearray(nbBytes)
        self.ser.readinto(rawData)
        # Convert the raw data
        data = Smdata(header + rawData)
        return data.info

    def writeData(self, data):
        rawData = Smdata(data).bytes
        self.ser.write(rawData)

    def close(self):
        self.ser.close()
