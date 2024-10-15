import socket
import bitStreamsSpring2024 as bitStreamsSpring2024
import threading
import queue
import pickle
import ploting


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


class ClientAgent(threading.Thread):
    def __init__(self, gas, rowsQueue):
        threading.Thread.__init__(self)
        self.serverAddress = ('localhost', 5000)
        self.gas = gas
        self.rowsQueue = rowsQueue
        self.results = {}

    def run(self):
        while not self.rowsQueue.empty():
            rowid = self.rowsQueue.get()
            result = self.queryServer(rowid, self.gas)
            if result is not None:
                self.results[rowid] = result
            self.rowsQueue.task_done()

    def queryServer(self, rowid, gas):
        try:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect(self.serverAddress)
            request = pickle.dumps((rowid, gas))
            clientSocket.send(request)
            response = clientSocket.recv(1024)
            result = pickle.loads(response)
            clientSocket.close()
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None

if __name__ == "__main__":
    rowsQueue = queue.Queue()

    for rowid in range(1, 45):
        rowsQueue.put(rowid)
        rowsQueue.put(rowid)
        rowsQueue.put(rowid)
        rowsQueue.put(rowid)
        rowsQueue.put(rowid)
        rowsQueue.put(rowid)

    gases = ['CO2', 'CH4', 'N2O', 'CFCs', 'HCFCs', 'HFCs']
    clients = [ClientAgent(gas, rowsQueue) for gas in gases]

    for client in clients:
        client.start()

    for client in clients:
        client.join()

    agentData = {client.gas: client.results for client in clients}
    print(agentData)

    LinearRegressionGraph = ploting.PlotManager(None, agentData)
    LinearRegressionGraph.plotAllGases()

