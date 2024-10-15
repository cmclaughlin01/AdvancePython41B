import sqlite3
import os


class dataBase:
    def __init__(self, dbName):
        self.dbName = dbName
        self.dbConnect = None
        self.cursor = None
        self.tableName = "tableData"
        self.tableColumns = {}
        self.count = 0
        self.query = ""
        self.data = None
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
        else:
            self.dbConnect = sqlite3.connect(self.dbName)
            self.cursor = self.dbConnect.cursor()
            print(f"The Database '{self.dbName}' has been created and connected to.")

    def createTable(self, data):
        self.tableColumns = data
        try:
            if isinstance(data, list):
                columnDefinitions = ', '.join([f"'{col}' TEXT" for col in data])
            else:
                print("Error")
            query = f'CREATE TABLE IF NOT EXISTS {self.tableName} ({columnDefinitions})'
            self.Execute(query)
        except sqlite3.Error as error:
            print(f"Failed to create sqlite table {error}")

    def insertData(self, data):
        try:
            columns = ', '.join(f'"{col}"' for col in self.tableColumns)  # Using the column names stored at index 2
            placeholders = ', '.join(['?' for _ in data])  # Create placeholders for each value
            query = f'INSERT INTO {self.tableName} ({columns}) VALUES ({placeholders})'
            self.query = query
            self.data = data
        except sqlite3.Error as error:
            print(f"Failed to insert data into sqlite table {error}")

    def selectData(self, data):
        try:
            query = f"SELECT {data} FROM {self.tableName}"
            self.query = query
        except sqlite3.Error as error:
            print(f"Failed to select data into sqlite table {error}")

    def findData(self, data):
        try:
            query = f'SELECT * FROM {self.tableName} WHERE {data}'
            self.query = query
            print(self.cursor.fetchall())
        except sqlite3.Error as error:
            print(f"Failed to find data from sqlite table {error}")

    def updateData(self, data):
        try:
            query = f"UPDATE {self.tableName} SET {data[0]} = ? WHERE {data[1]} = ?"
            self.query = query
            self.data = data[2]
        except sqlite3.Error as error:
            print(f"Failed to update data from sqlite table {error}")

    def deleteData(self, data):
        try:
            query = f"DELETE FROM {self.tableName} WHERE {data[0]} = ?"
            self.query = query
            self.data = data[1]
        except sqlite3.Error as error:
            print(f"Failed to delete data from sqlite table {error}")

    def testPrint(self):
        query = f"SELECT * FROM {self.tableName}"
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
        except sqlite3.Error as e:
            print(f"An error occurred when accessing the database: {e}")

    def checkColumns(self):
        query = "PRAGMA table_info(tableData);"
        self.cursor.execute(query)
        columns = self.cursor.fetchall()
        for column in columns:
            print(column)
