class rotatingCypher:
    def __init__(self):
        self.shift = 5
        self.text = ""
        self.encryptedData = ""
        self.decryptedData = ""
        self.lowerAscii = 0x20
        self.upperAscii = 0x80

    def encrypt(self, text):
        self.text = text
        self.encryptedData = ""  # Reset encrypted data
        currentShift = self.shift
        for char in text:
            if self.lowerAscii <= ord(char) <= self.upperAscii:
                shifted = ord(char) + currentShift
                if shifted >= self.upperAscii:
                    shifted = self.lowerAscii + (shifted - self.upperAscii)
                self.encryptedData += chr(shifted)
                currentShift += 1
            else:
                self.encryptedData += char
        return self.encryptedData

    def decrypt(self, text):
        self.text = text
        self.decryptedData = ""  # Reset decrypted data
        currentShift = self.shift
        for char in text:
            if self.lowerAscii <= ord(char) <= self.upperAscii:
                shifted = ord(char) - currentShift
                if shifted < self.lowerAscii:
                    shifted = self.upperAscii - (self.lowerAscii - shifted)
                self.decryptedData += chr(shifted)
                currentShift += 1
            else:
                self.decryptedData += char
        return self.decryptedData

if __name__ == "__main__":
    tester = rotatingCypher()
    testerEnc = tester.encrypt("011,3")
    print(testerEnc)
    testerDe = tester.decrypt(testerEnc)
    print(testerDe)
