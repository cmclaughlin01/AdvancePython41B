import baseXConverter

class baseXDigit:
    def __init__(self, number):
        self.converter = baseXConverter.BaseConverter()
        self.value = number
        self.base = None
        self.number = None
        self.baseTenNum = None
        self.makeBaseTen()

    def makeBaseTen(self):
        self.baseTenNum = self.converter.convert(self.value, 10)

    def getBase(self):
        try:
            if self.baseTenNum:
                self.base = self.converter.fromBase
                self.number = self.converter.fromNumber
                return self.base, self.number
        except Exception as e:
            print(f"Error: {e}")

    def __add__(self, other):
        valueOne = int(self.baseTenNum[2:])
        valueTwo = int(other.baseTenNum[2:])
        result = valueOne + valueTwo
        return f'0a{result}'

    def __sub__(self, other):
        valueOne = int(self.baseTenNum[2:])
        valueTwo = int(other.baseTenNum[2:])
        result = valueOne - valueTwo
        return f'0a{result}'

    def __mul__(self, other):
        valueOne = int(self.baseTenNum[2:])
        valueTwo = int(other.baseTenNum[2:])
        result = valueOne * valueTwo
        return f'0a{result}'

    def __truediv__(self, other):
        valueOne = int(self.baseTenNum[2:])
        valueTwo = int(other.baseTenNum[2:])
        result = valueOne / valueTwo
        return f'0a{result}'

    def __mod__(self, other):
        valueOne = int(self.baseTenNum[2:])
        valueTwo = int(other.baseTenNum[2:])
        result = valueOne % valueTwo
        return f'0a{result}'

if __name__ == "__main__":
    tester = baseXDigit("0M123")
    base = tester.getBase()
    print(base)
    print(tester.baseTenNum)

    tester2 = baseXDigit("0G1234")

    print(tester - tester2)
