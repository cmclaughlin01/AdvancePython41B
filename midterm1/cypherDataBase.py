# both dataBases and rotatingCaesarCypher will be included in the comments in a zip
import dataBases
import rotatingCaesarCypher

if __name__ == "__main__":
    # creates the dataBase and constructs the table
    cypherDataBase = dataBases.dataBase("cypherDataBase")
    cypherDataBase.queryBuilder("Create database", None)
    columnDefinitions = {0: ['Initial_text', 'Encrypted_text', 'Decrypted_text', 'Shift']}
    cypherDataBase.queryBuilder("Create table", columnDefinitions[0])
    cypherDataBase.checkColumns()

    # uses the cypher class to give some data to insert
    cipher = rotatingCaesarCypher.rotatingCypher(5)
    encrypted = cipher.encrypt("HELLO")
    cipher.decrypt(encrypted)

    # takes the data from above then creates the query to be encrypted
    row = {0: ["HELLO", cipher.encryptedData, cipher.decryptedData, cipher.shift]}
    cypherDataBase.queryBuilder("Insert", row[0])

    # Using the query from the queryBuilder the query value is pasted into the func
    # the query is taken init vars inside the dataBase class
    encryptedInsert = rotatingCaesarCypher.rotatingCypher(3)
    encrypted = encryptedInsert.encrypt(cypherDataBase.query)
    encryptedInsert.printEncrypt()
    encryptedInsert.decrypt(encrypted)
    encryptedInsert.printDecrypt()

    # once the query has been encrypted and then decrypted it is executed
    # both args are taken from the init vars of their classes
    cypherDataBase.Execute(encryptedInsert.decryptedData, cypherDataBase.data)

    # used to test that the insert function worked and the data is inside the db
    cypherDataBase.testPrint()

    cypherDataBase.disconnet()