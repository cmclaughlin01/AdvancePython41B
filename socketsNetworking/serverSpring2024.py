import socket
import bitStreamsSpring2024
import dataBases
import json

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
        self.serverDataBase = None
        self.createServerDB()
        self.acceptedSqlCommands = {
            "CREATE DATABASE", "CREATE TABLE", "INSERT", "SELECT",
            "FIND", "UPDATE", "DELETE"
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
        byteData = bitStreamsSpring2024.stringToByte(message)
        data = byteData.toByteArray()
        print(data)
        self.connection.sendall(data)
        self.checkCloseTag(message)

    def sendClientFile(self, fileName):
        with open(fileName, 'rb') as file:
            data = file.read(1024)
            while data:
                dataArray = bitStreamsSpring2024.stringToByte(data)
                arrayData = dataArray.toByteArray()
                self.connection.send(arrayData)
                print('Sent ', repr(arrayData))
                self.checkCloseTag(data)
                data = file.read(1024)

    def receiveFromClient(self):
        try:
            while True:
                print('receiving data...')
                messageLen = int(self.connection.recv(10).decode('utf-8').strip())
                data = self.connection.recv(messageLen).decode('utf-8')
                self.checkCloseTag(data)
                message = bitStreamsSpring2024.stringToByte(data)
                strMessage = message.fromByteArray()
                for word in self.acceptedSqlCommands:
                    if word in strMessage:
                        self.sqliteHandler(strMessage)
                if not data or self.closeConnection:
                    print("BREAKING")
                    break
            print('received {!r}'.format(data))
        except WindowsError as e:
            print(f"Error: {e}")

    def checkCloseTag(self, data):
        if not isinstance(data, str):
            strData = bitStreamsSpring2024.stringToByte(data)
            data = strData.fromBitString()
        if data.endswith(self.closingTag):
            print(f'The connection to {self.host} port {self.port} has been closed')
            self.closeConnection = True
            self.connection.close()

    def sqliteHandler(self, query):
        print(query)
        try:
            execQuery = self.serverDataBase.execute(query)
            # print(testResponse)
            uniqueData = []
            seen = set()
            for item in execQuery:
                tupleItem = tuple(item)
                if tupleItem not in seen:
                    seen.add(tupleItem)
                    uniqueData.append(item)
            cleanData = json.dumps(uniqueData)
            self.sendClientStr(cleanData)
        except Exception as e:
            print(f'Error handling sqlite3 command: {e}')

    def createServerDB(self):
        self.serverDataBase = dataBases.dataBase("serverDataBase")
        self.serverDataBase.queryBuilder("Create database", None)
        columnDefinitions2 = {0: ['id', 'name', 'age', 'department', 'salary']}
        self.serverDataBase.queryBuilder("CREATE TABLE", columnDefinitions2[0])


if __name__ == "__main__":
    testServer = serverSockets()
    testServer.serverConnect()

    try:
        testServer.sendClientStr("Whats up from the server")
        testServer.receiveFromClient()
    except Exception as e:
        print(f'Error: {e}')
