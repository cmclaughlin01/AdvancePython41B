class rotor:
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
            print(self.position)
            self.increment()
        else:
            rotated_char = chr((ord(char) - self.position - self.lowerAscii) % (self.upperAscii - self.lowerAscii)
                               + self.lowerAscii)
            self.increment()
        return rotated_char


class rotatingCypher:
    def __init__(self, shift):
        self.rotor = rotor(shift)
        self.text = ""
        self.encryptedData = ""
        self.decryptedData = ""

    def encrypt(self, text):
        self.text = text
        self.rotor.reset()
        for char in text:
            if 0x20 <= ord(char) < 0x80:
                rotated_char = self.rotor.rotate(char, True)
                self.encryptedData += rotated_char
            else:
                self.encryptedData += char
        return self.encryptedData

    def decrypt(self, text):
        self.text = text
        self.rotor.reset()
        for char in text:
            if 0x20 <= ord(char) < 0x80:
                rotated_char = self.rotor.rotate(char, False)
                self.decryptedData += rotated_char
            else:
                self.decryptedData += char
        return self.decryptedData

    def printEncrypt(self):
        print(f"- Encrypted message: '{self.encryptedData}'\n")

    def printDecrypt(self):
        print(f"- Decrypted message: '{self.decryptedData}'\n")



if __name__ == "__main__":
    cipher = rotatingCypher(5)
    stringToDo = "HELLO"
    encrypted = cipher.encrypt(stringToDo)
    cipher.printEncrypt()
    cipher.decrypt(encrypted)
    cipher.printDecrypt()
