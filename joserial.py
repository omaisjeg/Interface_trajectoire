#!/usr/bin/env python3
# modified version of https://github.com/JonathanPlasse/binary_serial

import serial
import time
from joformat import dataSize, formatDict, Smdata, bytes2Data


class Connection:
    def __init__(self, port='/dev/ttyACM0', baudRate=115200):
        self.ser = serial.Serial(port, baudRate, timeout=1)

    def readData(self, format):
        nbBytes = dataSize(formatDict[format])
        # Wait until all the data is in the buffer
        while self.ser.in_waiting < nbBytes:
            pass
        # Read the raw data
        rawData = bytearray(nbBytes)
        self.ser.readinto(rawData)
        # Convert the raw data
        data = bytes2Data(formatDict[format], rawData)
        return [format, data]

    def writeData(self, data):
        rawData = Smdata(data).raw
        self.ser.write(rawData)

    def close(self):
        self.ser.close()
