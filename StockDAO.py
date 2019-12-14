# Data Access Object Pattern or DAO pattern is used to separate low level data accessing API or operations from high level business services. Following are the participants in Data Access Object Pattern.
# Data Access Object Interface - This interface defines the standard operations to be performed on a model object(s).
# Data Access Object concrete class - This class implements above interface. This class is responsible to get data from a data source which can be database / xml or any other storage mechanism.
# Model Object or Value Object - This object is simple POJO containing get/set methods to store data retrieved using DAO class.

import mysql.connector
import dbconfig as cfg

class StockDAO:
    db = ""
    def initConnectToDB(self):
        db = mysql.connector.connect(
            host = cfg.mySQL['host'],
            user = cfg.mySQL['user'],
            password = cfg.mySQL['password'],
            database = cfg.mySQL['database'],
            pool_name = 'my_connection_pool',
            pool_size = 6
            # auth_plugin='mysql_native_password
            )
        return db

    def getConnection(self):
        db = mysql.connector.connect(
            pool_name = 'my_connection_pool',
            )
        return db

    def __init__(self):
       db = self.initConnectToDB()
       db.close

    def getCursor(self):
        # checks if database is connected,if no, get new cursor
        if not self.db.is_connected():
            self.connectToDB()
        return self.db.cursor()

    def create(self, values):
        # print(values)
        db = self.getConnection()
        cursor = db.cursor()
        sql = "insert into stock (Type, Title, Artist_Author, Genre, Quantity, Price, Discogs_GoodReadsID) values (%s, %s,%s, %s, %s, %s, %s)"
        cursor.execute(sql, values)
        db.commit()
        lastRowID = cursor.lastrowid
        db.close()
        return lastRowID

    def getAll(self):
        db = self.getConnection()
        cursor = db.cursor()
        sql = "select * from stock"
        cursor.execute(sql)
        data = cursor.fetchall()
        stockList =[]
        for row in data:
            stockList.append(self.convertToDictionary(row))
        db.close()
        return stockList
    
    def getByID(self, id):
        db = self.getConnection()
        cursor = db.cursor()
        sql = "select * from stock where id = %s"
        values = (id,)
        cursor.execute(sql,values)
        result = cursor.fetchone()
        db.close()
        return self.convertToDictionary(result)

    def update(self, values):
        db = self.getConnection()
        cursor = db.cursor()
        sql = "UPDATE stock SET Type = %s, Title = %s, Artist_Author = %s, Genre = %s, Quantity = %s, Price = %s, Discogs_GoodReadsID = %s WHERE id = %s"
        cursor.execute(sql,values)
        db.commit()
        # returns a json object, i.e convertToDictionary()
        db.close()
        return # self.convertToDictionary(values)
    
    def delete(self, id):
        db = self.getConnection()
        cursor = db.cursor()
        # likewise
        sql = "delete from stock where id = %s"
        value = (id,)
        cursor.execute(sql, value)
        db.commit()
        db.close()
        print("delete executed")
        return
    
    def convertToDictionary(self, result):
        cols = ['id', 'Type', 'Title', 'Artist_Author',  'Genre',  'Quantity', 'Price', 'Discogs_GoodReadsID']
        item = {}
        if result:
            for i, col in enumerate(cols):
                value = result[i]
                item[col] = value
        return(item)

stockDAO = StockDAO()
# values = (stockDAO.getAll())
# for value in values:
#    print(value)