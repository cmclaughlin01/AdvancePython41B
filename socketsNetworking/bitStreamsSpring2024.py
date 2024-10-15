import json
import struct
import pandas as pd
from bitstring import BitStream, BitArray, Bits

class stringToByte:
    def __init__(self, inputString):
        self.inputString = inputString
        self.userByte = None
        self.userByteArray = self.toByteArray()
        self.userBitString = self.toBitString()

    def __str__(self):
        return f"Stringsss"

    def __iter__(self):
        yield from{
            'input' : self.inputString
        }.iteams()

    def input(self):
        return self.inputString

    def input(self, newString):
        self.inputString = newString

    def toByte(self):
        try:
            if len(self.inputString) != 1:
                raise ValueError("String must be one character in length")
            # if not isinstance(self.inputString, str):
            #     raise TypeError(f"The input type {type(self.inputString)} is not supported please use strings")
            else:
                self.userByte = bytes(self.inputString, 'utf-8')
                return self.userByte
        except ValueError as e:
            print(f"Error: {e}")
            self.userByte = b''
            return self.userByte

    def toByteArray(self):
        try:
            if isinstance(self.inputString, str):
                self.userByteArray = bytearray(self.inputString, 'utf-8')
                return self.userByteArray
            elif isinstance(self.inputString, bytes):
                self.userByteArray = bytearray(self.inputString)
                return self.userByteArray
            else:
                raise TypeError(f"The input type {type(self.inputString)} is not supported please use strings or bytes")
        except TypeError as e:
            print(f"Error: {e}")
            self.userByteArray = bytearray(b'')
            return self.userByteArray

    def toBitString(self):
        try:
            if isinstance(self.inputString, str):
                bytesHolder = bytes(self.inputString, 'utf-8')
                self.userBitString = BitStream(bytesHolder)
                return self.userBitString
            elif isinstance(self.inputString, bytes):
                self.userBitString = BitStream(self.inputString)
                return self.userBitString
            else:
                raise TypeError(f"The input type {type(self.inputString)} is not supported please use strings or bytes")
        except TypeError as e:
            print(f'Error: {e}')
            self.userBitString = 0x00
            return self.userBitString

    def fromByte(self):
        try:
            if isinstance(self.userByte, bytes) and len(self.userByte) > 0:
                byteHolder = int.from_bytes(self.userByte, byteorder='big')
                self.userByte = chr(byteHolder)
                return self.userByte
            else:
                if len(self.userByte) < 1:
                    raise ValueError(f"The object is empty")
                else:
                    raise TypeError(f"The input type {type(self.inputString)} is not supported please use bytes")
        except ValueError as e:
            print(f'Error: {e}')
            return self.userByte
        except TypeError as e:
            print(f'Error: {e}')
            return self.userByte

    def fromByteArray(self):
        try:
            if isinstance(self.userByteArray, bytearray) and len(self.userByteArray) > 0:
                self.userByteArray = self.userByteArray.decode('utf-8')
                return self.userByteArray
            else:
                if len(self.userByteArray) < 1:
                    raise ValueError(f"The object is empty")
                else:
                    raise TypeError(f"The input type {type(self.inputString)} is not supported please use bytes")
        except ValueError as e:
            print(f'Error: {e}')
        except TypeError as e:
            print(f'Error: {e}')

    def fromBitString(self):
        try:
            if not isinstance(self.userBitString, bytes):
                self.userBitString = self.userBitString.tobytes()
            self.userBitString = self.userBitString.decode('utf-8')
            return self.userBitString
        except TypeError as e:
            print(f'Error: {e}')
        except ValueError as e:
            print(f'Error: {e}')
        except TypeError as e:
            print(f'Error: {e}')


if __name__ == "__main__":
    file = open('Frequencies.txt', 'rb')
    words = file.read()
    tester = stringToByte(words)
    testString = tester.toBitString()
    print(testString)
    print(tester.fromBitString())

    tester.input('H')
    print(tester.toByte())
    print(tester.fromByte())

    tester.input('Hello World')
    print(tester.toByteArray())
    print(tester.fromByteArray())

