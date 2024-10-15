import socket
import opCommand
import re
import Rotor
import caesarCypher

class serverSockets:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.serverNode = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverAddress = (self.host, self.port)
        self.connection = None
        self.clientAddress = None
        self.closeConnection = False
        self.closingTag = "close connection"
        self.vaildCommand = re.compile(r'^[01]{3},\d*$')
        self.rotor = Rotor.Rotor()
        self.encryption = caesarCypher.rotatingCypher()
        self.opcodeStr = {
            0b000: "Reset or initialize all counters to the default state for the rotor.",
            0b001: "Increment the rotor. Returns the incremented character.",
            0b010: "Decrement the rotor. Returns the decremented character.",
            0b011: "Execute either 0b001 or 0b010 N times depending on +/-N.",
            0b100: "Returns the current rotor position index.",
            0b101: "Returns the character at 0b100 position.",
            0b110: "Increments a rotation counter every time a rotor completes one rotation.",
            0b111: "TBD"
        }

    def serverConnect(self):
        print(f'starting up on {self.host} port {self.port}')
        self.serverNode.bind(self.serverAddress)
        self.serverNode.listen(1)
        print('Waiting for a connection')
        self.connection, self.clientAddress = self.serverNode.accept()
        print(f'Connection from {self.clientAddress}')

    def sendClientStr(self, message):
        print('sending {!r}'.format(message))
        data = message.encode('utf-8')
        messageLen = len(data)
        data = f"{messageLen:<10}".encode('utf-8') + data
        print(data)
        self.connection.sendall(data)
        self.checkCloseTag(message)

    def sendClientFile(self, fileName):
        with open(fileName, 'rb') as file:
            data = file.read(1024)
            while data:
                self.connection.send(data)
                print('Sent ', repr(data))
                self.checkCloseTag(data)
                data = file.read(1024)

    def receiveFromClient(self):
        try:
            while True:
                print('receiving data...')
                messageLen = int(self.connection.recv(10).decode('utf-8').strip())
                data = self.connection.recv(messageLen).decode('utf-8')
                data = self.encryption.decrypt(data)
                if self.vaildCommand.match(data):
                    command = self.parseCommand(data)
                    self.opCode = command.op
                    self.runCommand(command)
                self.checkCloseTag(data)
                if not data or self.closeConnection:
                    print("BREAKING")
                    break
                print('received {!r}'.format(data))
        except WindowsError as e:
            print(f"Error: {e}")

    def parseCommand(self, data):
        parts = data.split(',')
        op = int(parts[0], 2)
        argv = int(parts[1]) if len(parts) > 1 and parts[1] else None
        return opCommand.Command(op, argv)

    def runCommand(self, command):
        commandOut = self.rotor.handleCommand(command)
        if command.op in self.opcodeStr:
            commandStr = f'{commandOut} - {self.opcodeStr[command.op]}'
        else:
            commandStr = str(commandOut)
        self.sendClientStr(commandStr)

    def checkCloseTag(self, data):
        if not isinstance(data, str):
            data = data.decode('utf-8')
        if data.endswith(self.closingTag):
            print(f'The connection to {self.host} port {self.port} has been closed')
            self.closeConnection = True
            self.connection.close()

if __name__ == "__main__":
    testServer = serverSockets()
    testServer.serverConnect()

    try:
        testServer.sendClientStr("Whats up from the server")
        testServer.receiveFromClient()
    except Exception as e:
        print(f'Error: {e}')
