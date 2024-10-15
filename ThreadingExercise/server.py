from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import defaultdict
from pathlib import Path
import pandas as pd
import dataBases
import socket
import bitStreamsSpring2024
import webScraping
import json
import threading
import pickle
import sqlite3


class serverSockets(threading.Thread):
    def __init__(self, db, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.serverNode = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverAddress = (self.host, self.port)
        self.connection = None
        self.clientAddress = None
        self.closeConnection = False
        self.closingTag = "close connection"
        self.serverDataBase = None
        #self.createServerDB(db)
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

    def createServerDB(self, db):
        self.serverDataBase = dataBases.dataBase("serverDataBase")
        self.serverDataBase.queryBuilder("Create database", None)
        columnDefinitions = []
        for i,column in enumerate(db):
            columnDefinitions.append(column)
        self.serverDataBase.queryBuilder("CREATE TABLE", columnDefinitions)
        self.serverDataBase.queryBuilder("INSERT", db)


class DataBaseServer:
    def __init__(self, dbName="threadingDataBase"):
        self.conn = sqlite3.connect(dbName, check_same_thread=False)
        self.lock = threading.Lock()

    def query(self, rowid, gas):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT {gas} FROM tableData WHERE rowid=?", (rowid,))
            result = cursor.fetchone()
            return result[0] if result else None

    def close(self):
        self.conn.close()


def handleClientConn(clientSocket, dbServer):
    while True:
        try:
            request = clientSocket.recv(1024)
            if not request:
                break
            rowid, gas = pickle.loads(request)
            result = dbServer.query(rowid, gas)
            clientSocket.send(pickle.dumps(result))
        except Exception as e:
            print(f"Error: {e}")
            break
    clientSocket.close()

if __name__ == "__main__":
    url = 'https://gml.noaa.gov/aggi/aggi.html'

    scrap = webScraping.webScraping(url, "tbody", None)
    scrap.run()

    threadingPanda = scrap.getPanda()
    print(threadingPanda.columns)

    threadingDataBase = dataBases.dataBase("threadingDataBase")
    threadingDataBase.queryBuilder("Create database", None)
    columnDefinitions = []
    for i,column in enumerate(threadingPanda.columns):
        columnDefinitions.append(column)
    threadingDataBase.queryBuilder("Create table", columnDefinitions)
    threadingDataBase.checkColumns()

    for i in range(0, len(threadingPanda)):
        row = threadingPanda.iloc[i].tolist()
        threadingDataBase.queryBuilder("Insert", row)

    dbServer = DataBaseServer()
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('0.0.0.0', 5000))
    serverSocket.listen(5)
    print("Server listening on port 5000")

    while True:
        clientSocket, addr = serverSocket.accept()
        print(f"Accepted connection from {addr}")
        clientHandler = threading.Thread(
            target=handleClientConn, args=(clientSocket, dbServer)
        )
        clientHandler.start()

