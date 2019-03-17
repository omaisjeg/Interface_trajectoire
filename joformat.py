import struct

typesDict = {'char': 'c', 'bool': '?',
             'int8': 'b', 'uint8': 'B',
             'int16': 'h', 'uint16': 'H',
             'int32': 'i', 'uint32': 'I',
             'int64': 'l', 'uint64': 'L',
             'float': 'f'}

structFormatConfig = ['uint8', 'uint16', 'uint16', 'uint8']
structFormatMeasure = ['uint32', 'uint32', 'float']


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
