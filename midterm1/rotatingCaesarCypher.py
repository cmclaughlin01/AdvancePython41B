class rotatingCypher:
    def __init__(self, shift):
        self.shift = shift
        self.text = ""
        self.encryptedData = ""
        self.decryptedData = ""
        self.lowerAscii = 0x20
        self.upperAscii = 0x80

    def encrypt(self, text):
        self.text = text
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

    def printEncrypt(self):
        print(f"- Given ascii text:'{self.text}'")
        print(f"- Initial Shift value:'{self.shift}'")
        print(f"- Encryption:")
        for char in range(len(self.text)):
            shift = ord(self.encryptedData[char]) - ord(self.text[char])
            print(f"    - {self.text[char]} becomes {self.encryptedData[char]} "
                  f"(shift {shift} from {self.text[char]})")
        print(f"- Encrypted message: '{self.encryptedData}'\n")

    def printDecrypt(self):
        # print(f"- Given ascii text:'{self.text}'")
        # print(f"- Initial Shift value:'{self.shift}'")
        # print(f"- Decryption:")
        # for char in range(len(self.text)):
        #     shift = ord(self.decryptedData[char]) - ord(self.text[char])
        #     print(f"    - {self.text[char]} becomes {self.decryptedData[char]} "
        #           f"(shift {shift} from {self.text[char]})")
        print(f"- Decrypted message: '{self.decryptedData}'\n")



if __name__ == "__main__":
    cipher = rotatingCypher(3)
    stringToDo = "HELLO"
    encrypted = cipher.encrypt(stringToDo)
    cipher.printEncrypt()
    cipher.decrypt(encrypted)
    cipher.printDecrypt()
