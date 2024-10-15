import socket
import bitStreamsSpring2024


class clientSockets:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.clientNode = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverAddress = (self.host, self.port)

    def clientConnect(self):
        print(f'Connecting to {self.host} port {self.port}')
        self.clientNode.connect(self.serverAddress)

    def sendServerStr(self, message):
        print('sending {!r}'.format(message))
        byteData = bitStreamsSpring2024.stringToByte(message)
        data = byteData.toByteArray()
        messageLen = len(data)
        data = f"{messageLen:<10}".encode('utf-8') + data
        self.clientNode.sendall(data)

    def sendServerFile(self, fileName):
        with open(fileName, 'rb') as file:
            data = file.read(1024)
            while data:
                dataArray = bitStreamsSpring2024.stringToByte(data)
                arrayData = dataArray.toByteArray()
                messageLen = len(data)  # updated
                arrayData = f"{messageLen:<10}".encode('utf-8') + arrayData
                self.clientNode.send(arrayData)
                print('Sent ', repr(arrayData))
                data = file.read(1024)

    def receiveFromServer(self):
        try:
            while True:
                data = self.clientNode.recv(1024)
                if not data:
                    break
                strData = bitStreamsSpring2024.stringToByte(data)
                data = strData.fromBitString()
                if len(data) > 4:
                    print('received {!r}'.format(data))
        except WindowsError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    testClient = clientSockets()
    testClient.clientConnect()
    try:
        testClient.sendServerStr('''INSERT INTO tableData (id, name, age, department, salary) VALUES ('1', 'John Doe', '30', 'Engineering', '70000'), ('2', 'Jane Smith', '25', 'Marketing', '60000'), ('3', 'Sam Brown', '35', 'Sales', '80000'), ('4', 'Nancy Wilson', '28', 'Human Resources', '65000'), ('5', 'Paul Johnson', '40', 'Finance', '90000')''')
        testClient.sendServerStr('''SELECT name FROM tableData''')
        testClient.sendServerStr("it has been nice")
        testClient.sendServerStr("close connection")
        testClient.receiveFromServer()
    except Exception as e:
        print(f'Error: {e}')
