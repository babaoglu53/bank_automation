import mysql.connector

class Database():
    def __init__(self, host, port, username, password, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

        self.mydb = mysql.connector.connect(
            host = self.host,
            port = self.port,
            user = self.username,
            password = self.password,
            database = self.database
        )
        
    
    def disconnectDatabase(self):
        self.mydb.close()

    def getCursor(self, database_connection):
        return database_connection.cursor()

    def selectQuery(self, select_par, from_par, cursor, range, where_par = None, where_args = ()):
        if where_par == None:
            cursor.execute("SELECT " + select_par + " FROM " + from_par)
        else:
            cursor.execute("SELECT " + select_par + " FROM " + from_par + " WHERE " + where_par, where_args)
        
        if range == "all":
            result = cursor.fetchall()
        if range == "one":
            result = cursor.fetchone()

        return result

    def insertQuery(self, into_par, column_names, values_for_percent, values, cursor):
        query = ("INSERT INTO " + into_par + " " + column_names + " VALUES " + values_for_percent)
        try:
            cursor.execute(query, values)
            self.mydb.commit()
        except:
            self.mydb.rollback()

    def executeQuery(self, query, cursor):
        try:
            cursor.execute(query)
            self.mydb.commit()
        except:
            self.mydb.rollback()

    def dateQuery(self, query, cursor):
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def insertToTransactions(self, account_no, transaction_name, amount, cursor):
        self.insertQuery("transactions", "(account_no, transaction_name, amount)", "(%s, %s, %s)", (account_no, transaction_name, amount), cursor)

    def otherSelectQuery(self, query, cursor, range):
        cursor.execute(query)
        
        if range == "all":
            result = cursor.fetchall()
        if range == "one":
            result = cursor.fetchone()
        
        return result
