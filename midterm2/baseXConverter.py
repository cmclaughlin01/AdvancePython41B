import re


class BaseConverter:
    def __init__(self):
        self.baseRange = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.fromValue = None
        self.toValue = None
        self.convertedNum = None
        self.valid = True
        self.fromBase = None
        self.fromNumber = None
        self.toBase = None
        self.toNumber = None

    def baseValue(self, char):
        return self.baseRange.index(char)

    def checkValidForm(self):
        try:
            validForm = re.match(r'0([0-9A-Za-z])([0-9A-Za-z]+)', self.fromValue)
            if not validForm:
                self.valid = False
                raise ValueError(f"The number format {self.fromValue} does not follow 0A1234")
            if isinstance(self.toValue, str):
                self.toValue = self.baseValue(self.toValue.upper())
            if not (2 <= self.toValue <= 35):
                self.valid = False
                raise ValueError(f"The base range must be within 2 and 35")
            self.fromBase = validForm.group(1)
            self.fromNumber = validForm.group(2)
            return self.fromBase, self.fromNumber
        except ValueError as e:
            print(f"Error: {e}")

    def commonBase(self, value, base):
        value = value.upper()
        commonBase = 0
        for i, char in enumerate(reversed(value)):
            value = self.baseValue(char)
            commonBase += value * (base ** i)
        return commonBase

    def toNewBase(self, commonBase, toBase):
        result = ''
        self.toBase = self.baseRange[toBase].lower()
        while commonBase > 0:
            result = self.baseRange[commonBase % toBase] + result
            commonBase //= toBase
        self.toNumber = result
        self.convertedNum = '0' + self.toBase + result
        return self.convertedNum

    def printConvert(self):
        print(f"Converting {self.fromValue} to {self.convertedNum} (base{self.fromBase} to base{self.toBase.upper()})")

    def convert(self, fromBase, toBase):
        self.fromValue = fromBase
        self.toValue = toBase
        self.checkValidForm()
        try:
            if self.valid:
                base = self.baseValue(self.fromBase)
                value = self.commonBase(self.fromNumber, base)

                self.toNewBase(value, self.toValue)
                self.printConvert()
                return self.convertedNum
        except Exception as e:
            print(f'Error: {e}')


if __name__ == "__main__":
    convert = BaseConverter()
    convert.convert('0E12345', 'Z')
    convert.convert('0Z3F', 'q')
    convert.convert('0G10', 'a')
    convert.convert('0I12GGH', 'z')
