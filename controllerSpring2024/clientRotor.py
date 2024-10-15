import socket
import opCommand
import caesarCypher

class clientSockets:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.clientNode = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverAddress = (self.host, self.port)
        self.encryption = caesarCypher.rotatingCypher()

    def clientConnect(self):
        print(f'Connecting to {self.host} port {self.port}')
        self.clientNode.connect(self.serverAddress)
        print(f'Connected to {self.host} port {self.port}')

    def sendServerStr(self, message):
        print('sending {!r}'.format(message))
        message = self.encryption.encrypt(message)
        data = message.encode('utf-8')
        messageLen = len(data)
        data = f"{messageLen:<10}".encode('utf-8') + data
        self.clientNode.sendall(data)

    def sendServerFile(self, fileName):
        with open(fileName, 'rb') as file:
            data = file.read(1024)
            while data:
                messageLen = len(data)
                arrayData = f"{messageLen:<10}".encode('utf-8') + data
                self.clientNode.send(arrayData)
                print('Sent ', repr(arrayData))
                data = file.read(1024)


    def sendCommand(self, command):
        commandStr = f"{command.op:03b},{command.argv if command.argv is not None else ''}"
        print(commandStr)
        encryptedCommand = self.encryption.encrypt(commandStr)
        print(encryptedCommand)
        encryptedCommand = f"{len(encryptedCommand):<10}" + encryptedCommand
        self.clientNode.send(encryptedCommand.encode('utf-8'))
        print(f'Sent command: {encryptedCommand}')

    def receiveFromServer(self):
        try:
            while True:
                print('receiving data...')
                messageLen = int(self.clientNode.recv(10).decode('utf-8').strip())
                data = self.clientNode.recv(messageLen).decode('utf-8')
                if not data:
                    print("BREAKING")
                    break
                print('received {!r}'.format(data))
        except WindowsError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    testClient = clientSockets()
    testClient.clientConnect()
    try:
        cmdIncrementMult = opCommand.Command(0b011, 5)
        testClient.sendCommand(cmdIncrementMult)
        cmdDecrement = opCommand.Command(0b010)
        testClient.sendCommand(cmdDecrement)
        cmdGetIndexPos = opCommand.Command(0b101, 2)
        testClient.sendCommand(cmdGetIndexPos)
        cmdCounter = opCommand.Command(0b110)
        testClient.sendCommand(cmdCounter)
        testClient.sendServerStr("close connection")
        testClient.receiveFromServer()
    except Exception as e:
        print(f'Error: {e}')
