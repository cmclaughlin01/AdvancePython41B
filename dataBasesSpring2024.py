import sqlite3
import os
from bs4 import BeautifulSoup
from collections import defaultdict
from pathlib import Path
import pandas as pd


class dataBase:
    def __init__(self, dbName):
        self.dbName = dbName
        self.dbConnect = None
        self.cursor = None
        self.tableName = "tableData"
        self.count = 0
        self.queries = {
            "CREATE DATABASE": self.createDataBase,
            "CREATE TABLE": self.createTable,
            "INSERT": self.insertData,
            "SELECT": self.selectData,
            "FIND": self.findData,
            "UPDATE": self.updateData,
            "DELETE": self.deleteData
        }

    def queryBuilder(self, query, data):
        query_method = self.queries.get(query.upper())
        if query_method:
            query_method(data)
        else:
            if self.dbConnect is None:
                print("The Database was not found")
            else:
                print("The queryBuilder was unable to find a match for your request")
                print("Please try: CREATE DATABASE, CREATE TABLE, INSERT, SELECT, FIND, UPDATE, DELETE")
            return None

    def disconnet(self):
        self.dbConnect.close()
        print(f"{self.dbName} closed")
        os.remove(self.dbName)
        return 0

    def Execute(self, query="", tup=()):
        cursor = None
        try:
            print(f"Execute query: {query}")
            self.cursor.execute(query, tup)
            self.dbConnect.commit()
            print(f"Query executed")
        except sqlite3.Error as error:
            print(f"Query error: {error}")

        return cursor

    def createDataBase(self, data):
        if os.path.exists(self.dbName):
            self.dbConnect = sqlite3.connect(self.dbName)
            self.cursor = self.dbConnect.cursor()
            print(f"The Database '{self.dbName}' already exists, and now connected.")
            record = self.cursor.fetchall()
            print(f"Version is: {record}")
        else:
            self.dbConnect = sqlite3.connect(self.dbName)
            self.cursor = self.dbConnect.cursor()
            print(f"The Database '{self.dbName}' has been created and connected to.")
            record = self.cursor.fetchall()
            print(f"Version is: {record}")

    def createTable(self, data):
        try:
            if isinstance(data, list):
                column_definitions = ', '.join([f"'{col}' TEXT" for col in data])
            else:
                print("Error")
            query = f'CREATE TABLE IF NOT EXISTS {self.tableName} ({column_definitions})'
            self.Execute(query)
        except sqlite3.Error as error:
            print(f"Failed to create sqlite table {error}")

    def insertData(self, data):
        try:
            columns = ', '.join(f'"{col}"' for col in scrap.cleanTagData[2])  # Using the column names stored at index 2
            placeholders = ', '.join(['?' for _ in data])  # Create placeholders for each value
            query = f'INSERT INTO {self.tableName} ({columns}) VALUES ({placeholders})'
            self.Execute(query, data)
        except sqlite3.Error as error:
            print(f"Failed to insert data into sqlite table {error}")

    def selectData(self, data):
        try:
            query = f"SELECT {data} FROM {self.tableName}"
            self.Execute(query)
        except sqlite3.Error as error:
            print(f"Failed to select data into sqlite table {error}")

    def findData(self, data):
        try:
            query = f'SELECT * FROM {self.tableName} WHERE {data}'
            self.Execute(query)
            print(self.cursor.fetchall())
        except sqlite3.Error as error:
            print(f"Failed to find data from sqlite table {error}")

    def updateData(self, data):
        try:
            query = f"UPDATE {self.tableName} SET {data[0]} = ? WHERE {data[1]} = ?"
            self.Execute(query, data[2])
        except sqlite3.Error as error:
            print(f"Failed to update data from sqlite table {error}")

    def deleteData(self, data):
        try:
            query = f"DELETE FROM {self.tableName} WHERE {data[0]} = ?"
            self.Execute(query,data[1])
        except sqlite3.Error as error:
            print(f"Failed to delete data from sqlite table {error}")

class webScraping:

    def __init__(self, url, tagName, tagClass):
        self.url = url
        self.tagName = tagName
        self.tagClass = tagClass
        self.content = None
        self.rawTagData = None
        self.cleanTagData = None
        self.panda = None

    def parseData(self):
        file = Path(__file__).with_name(self.url)
        with open(file, "r") as fileOpen:
            fileContents = fileOpen.read()
            self.content = BeautifulSoup(fileContents, 'html.parser')
        # print(self.content)

    def extractTags(self):
        if self.content is not None:
            extractedTags = self.content.find(self.tagName, class_=self.tagClass)
            self.rawTagData = extractedTags
            # print(self.rawTagData)
        else:
            return None

    def cleanTags(self):
        rows = self.rawTagData.find_all('tr')
        cleanDict = defaultdict(dict)
        index = 0

        for row in rows:
            columns = row.find_all(['td'])
            colData = []

            for col in columns:
                data = col.text.strip()
                colData.append(data)

            cleanDict[index] = colData
            index += 1

        self.cleanTagData = cleanDict

    def run(self):
        try:
            self.parseData()
            if self.content:
                self.extractTags()
                self.cleanTags()
        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    fileName = 'Co2.html'

    scrap = webScraping(fileName, "table", None)
    scrap.run()

    print(scrap.cleanTagData)

    Co2Database = dataBase("Co2Database.db")
    Co2Database.queryBuilder("Create database", None)
    Co2Database.queryBuilder("Create table", scrap.cleanTagData[2])

    print(len(scrap.cleanTagData))
    for i in range(3, len(scrap.cleanTagData) - 400):
        row = scrap.cleanTagData[i]
        print(row)
        Co2Database.queryBuilder("Insert", row)

    findData = ("decimal = '2002.208'")
    Co2Database.queryBuilder("find", findData)

    deleteData = ("month", "3")
    Co2Database.queryBuilder("delete", deleteData)

    findData = ("trend = '372.44'")
    Co2Database.queryBuilder("find", findData)

    Co2Database.disconnet()

