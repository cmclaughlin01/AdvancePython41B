import json
import struct
import pandas as pd
from bitstring import BitStream, BitArray, Bits


def BinHexDec():
    print("hex\tbin\tdec")
    for x in range(0x11):
        print("{:x}\t{:b}\t{}".format(x, x, x))


def BitAnd(a, b):
    for i in [0, 1]:
        for j in [0, 1]:
            print("{} & {} = {}".format(i, j, i & j))
    print("{:b} & {:b} = {:b}\n".format(a, b, a & b))


def BitOr(a, b):
    for i in [0, 1]:
        for j in [0, 1]:
            print("{} | {} = {}".format(i, j, i | j))
    print("{:b} | {:b} = {:b}\n".format(a, b, a | b))


def BitEor(a, b):
    for i in [0, 1]:
        for j in [0, 1]:
            print("{:b} ^ {:b} = {:b}".format(i, j, i ^ j))
    print("{:b} ^ {:b} = {:b}\n".format(a, b, a ^ b))


def LowerAsciiPrintable():
    print("\nLower ASCII/Hex characters")
    [print(chr(i), '\t', hex(i).upper()) for i in range(32, 128)]


def RightShift(x, y):
    return x >> y


def LeftShift(x, y):
    return x << y


def TrueFalse(bval):
    if bval == False:
        print(False)
    if bval == True:
        print(True)


def Nibble(byte):
    print("original: ", bin(byte))
    lower = byte & 0b00001111
    upper = (byte & 0b11110000) >> 4
    print("  lower: ", format(lower, '04b'))
    print("  upper: ", format(upper, '04b'))
    return (bin(lower), bin(upper))


def Bytes2Bits(bdata):
    bigData = bin(int.from_bytes(bdata, byteorder='big'))[2:]
    print(bigData)
    litData = bin(int.from_bytes(bdata, byteorder='little'))[2:]
    print(litData)
    return bigData, litData


def ByteFile(filePath):
    afile = open(filePath, 'rb')
    bdata = bytearray(afile.read())
    return bdata


def BaseNumber(number):
    ba = BitArray(uint=number, length=12)
    print('binary: ', ba.bin)
    print('octal: ', ba.oct)
    print('dec: ', ba.int)
    print('hex: ', ba.hex)


def bsVideo(videofile):
    from bitstring import ConstBitStream
    info = []
    nbytes = 255
    with open(videofile, 'rb') as vfile:
        packet = ConstBitStream(bytes=vfile.read(nbytes), length=nbytes * 8)
        while (packet.pos < nbytes * 8):
            byte = packet.read(8).uint
            info.append(chr(byte))
        print(info)


def bsFile(filename):
    from bitstring import ConstBitStream
    info = []
    nbytes = 255
    with open(filename, 'rb') as vfile:
        packet = ConstBitStream(bytes=vfile.read(nbytes), length=nbytes * 8)
        while (packet.pos < nbytes * 8):
            byte = packet.read(8).uint
            info.append(chr(byte))
        print(info)


def bitTest():
    p1 = 15
    p2 = 7
    BitAnd(p1, p2)
    BitOr(p1, p2)
    BitEor(p1, p2)
    BinHexDec()
    LowerAsciiPrintable()
    number = 255
    shift = 3
    print(bin(RightShift(number, shift)))
    print(bin(LeftShift(number, shift)))
    byte = 123
    print(Nibble(byte))


def validate():
    bitTest()

    bdata = b'\x00\x0F\xF0\x0FF'
    print(bytes(bdata))
    print(Bytes2Bits(bdata))

    number = 8
    size = 4
    bnumber = number.to_bytes(size, 'big')
    print(f"Big: {number} = {bnumber}")
    lnumber = number.to_bytes(size, 'little')
    print(f"Little: {number} = {lnumber}")

    astr = "Hello World"
    btxt = bytes(astr, 'utf-8')
    print(btxt)

    hstr = "000FF0FF"
    bstr = bytes.fromhex(hstr)
    print(bstr)

    adct = {'Dwarf': {'0': 'Ceres', '1': 'Pluto', '2': 'Haumea', '3': 'Makemake', '4': 'Eris'},
            'AU': {'0': 2.77, '1': 39.5, '2': 43.19, '3': 45.48, '4': 67.84},
            'Years': {'0': 4.61, '1': 247.69, '2': 283.84, '3': 306.17, '4': 558.77}}
    jdct = json.dumps(adct)
    bdct = bytes(jdct, 'utf-8')
    print(bdct)

    dframe = pd.DataFrame(adct)
    bframe = bytes(dframe.to_json(), 'utf-8')
    print(bframe)

    abyte = b'\x41'  # ascii 'A'
    bary = bytearray(abyte)
    print(bary)

    alist = []
    [alist.append(i) for i in range(ord('A'), ord('Z'))]
    balist = bytes(alist)
    print(balist)
    bary = bytearray(alist)
    print(bary)
    abyte = bytes(bary)
    print(abyte)

    btxt = ByteFile('Frequencies.txt')
    print(btxt)
    bstream = BitStream(btxt)
    print(bstream)
    print('___________________')
    print(type(bstream))

    number = 255
    BaseNumber(number)

    print(25 * '-')
    bsFile('syllabus.txt')

    print(25 * '-')
    bsVideo('video.mp4')

    return True


import unittest


class Tests(unittest.TestCase):
    def test(self):
        assert (validate() == True)


if __name__ == '__main__':
    unittest.main()