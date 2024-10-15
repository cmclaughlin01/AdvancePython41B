import string
from collections import defaultdict


class Rotor:
    def __init__(self, initShift):
        self.lowerAscii = 0x20
        self.upperAscii = 0x80
        self.initShift = initShift
        self.position = initShift
        self.counter = 0

    def reset(self):
        self.counter = 0
        self.position = self.initShift

    def increment(self):
        self.position += 1
        if self.position >= self.upperAscii:
            self.position = self.lowerAscii
            self.counter += 1

    def decrement(self):
        self.position -= 1
        if self.position < self.lowerAscii:
            self.position = self.upperAscii - 1
            self.counter -= 1

    def rotate(self, char, encrypt):
        if encrypt:
            rotated_char = chr((ord(char) + self.position - self.lowerAscii) % (self.upperAscii - self.lowerAscii)
                               + self.lowerAscii)
            self.increment()
        else:
            rotated_char = chr((ord(char) - self.position - self.lowerAscii) % (self.upperAscii - self.lowerAscii)
                               + self.lowerAscii)
            self.increment()
        return rotated_char

    def rotateNoInc(self, char, encrypt):
        if encrypt:
            rotated_char = chr((ord(char) + self.position - self.lowerAscii) % (self.upperAscii - self.lowerAscii)
                               + self.lowerAscii)
        else:
            rotated_char = chr((ord(char) - self.position - self.lowerAscii) % (self.upperAscii - self.lowerAscii)
                               + self.lowerAscii)
        return rotated_char


def decryptText(text, rotor1Shift, rotor2Shift):
    rotor1 = Rotor(ord(rotor1Shift))
    rotor2 = Rotor(ord(rotor2Shift))

    decryptedText = []

    for i, char in enumerate(text):
        temp_char = rotor1.rotate(char, encrypt=False)
        decrypted_char = rotor2.rotateNoInc(temp_char, encrypt=False)
        decryptedText.append(decrypted_char)

        if (i + 1) % 95 == 0:
            rotor1.reset()
            rotor2.increment()
            rotor1 = Rotor(rotor1.initShift + rotor2.counter)

    return ''.join(decryptedText)


def countSigWords(decryptedText):
    commonWords = {"THE", "AND", "OF", "TO", "A", "IN", "IS", "IT", "YOU", "THAT"}
    words = decryptedText.split()
    
    wordCount = sum(word.upper() in commonWords for word in words)
    whitespaceCount = decryptedText.count(' ')

    return wordCount, whitespaceCount


if __name__ == "__main__":
    with open('E2Rotor.txt', 'r') as file:
        text = file.read()

    results = defaultdict(lambda: {'wordCount': 0, 'whitespaceCount': 0})

    for rotor1Shift in range(0x20, 0x80):
        for rotor2Shift in range(0x20, 0x80):
            decryptedText = decryptText(text, chr(rotor1Shift), chr(rotor2Shift))
            wordCount, whitespaceCount = countSigWords(decryptedText)
            results[(chr(rotor1Shift), chr(rotor2Shift))]['wordCount'] = wordCount
            results[(chr(rotor1Shift), chr(rotor2Shift))]['whitespaceCount'] = whitespaceCount

    bestSetting = max(results, key=lambda k: (results[k]['wordCount'], results[k]['whitespaceCount']))

    print(f'Best Rotor1 initial: {hex(ord(bestSetting[0]))}, Best Rotor2 initial: {hex(ord(bestSetting[1]))}')
    decryptedText = decryptText(text, bestSetting[0], bestSetting[1])
    for i in range(0, len(decryptedText), 120):
        print(decryptedText[i:i + 120])
