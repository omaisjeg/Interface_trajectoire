#!/usr/bin/env python3
import struct

typesDict = {'char': 'c', 'bool': '?',
             'int8': 'b', 'uint8': 'B',
             'int16': 'h', 'uint16': 'H',
             'int32': 'i', 'uint32': 'I',
             'int64': 'l', 'uint64': 'L',
             'float': 'f'}

structFormatConfig = ['uint8', 'uint16', 'uint16', 'uint8']
structFormatMeasure = ['uint32', 'uint32', 'float']

formatDict = {'c': structFormatConfig,
              'm': structFormatMeasure}


def computeFormat(structFormat):
    """Compute the format string for struct.(pack/unpack)"""
    structTypes = '='

    for t in structFormat:
        structTypes += typesDict[t]

    return structTypes


def data2Bytes(structFormat, data):
    structTypes = computeFormat(structFormat)
    rawData = struct.pack(structTypes, *data)
    return rawData


def bytes2Data(structFormat, rawData):
    structTypes = computeFormat(structFormat)
    data = list(struct.unpack(structTypes, rawData))
    return data


def dataSize(structFormat):
    structTypes = computeFormat(structFormat)
    return struct.calcsize(structTypes)


class Smdata:
    def __init__(self, arg):
        if isinstance(arg, (bytearray,bytes)):
            if arg[0] != 62 or arg[2] != 60:
                print(arg)
                raise 'ERROR MSG CORROMPU'
            self.bytes = arg
            self.name = arg[1:2].decode('ASCII')
            self.format = formatDict[self.name]
            self.raw = arg[3:]
            self.data = bytes2Data(self.format, self.raw)
            self.info = [self.name, self.data]
        if isinstance(arg, (list, tuple)):
            self.info = list(arg)
            self.name, self.data = arg
            self.format = formatDict[self.name]
            self.raw = data2Bytes(self.format, self.data)
            tmp = ">" + self.name + "<"
            self.bytes = tmp.encode('ASCII') + self.raw
