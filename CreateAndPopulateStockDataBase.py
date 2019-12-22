import mysql.connector
import dbconfig as cfg

mydb= mysql.connector.connect(
        host = cfg.mySQL['host'],
        user = cfg.mySQL['user'],
        password = cfg.mySQL['password'],
        # database = "datarepresentation",
        # auth_plugin='mysql_native_password'
        )

myCursor = mydb.cursor()

# create database
# sql= "DROP DATABASE shop" # deletes old database
# myCursor.execute("DROP DATABASE IF EXISTS davidsheils$shop")
# myCursor.execute("CREATE DATABASE davidsheils$shop")
# mydb.commit()
# print("Database Created")
myCursor.execute("USE davidsheils$shop")
# create stock table
print("Create table")
try:
    myCursor.execute("DROP TABLE IF EXISTS stock")
    myCursor.execute("CREATE TABLE stock(id int AUTO_INCREMENT PRIMARY KEY, Type VARCHAR(15), Title VARCHAR(255), Artist_Author VARCHAR(255), Genre VARCHAR(25), Quantity int, Price double, Discogs_GoodReadsID int)")
except Error as err:
    print(err)

from StockDAO import stockDAO
import csv

# import stock from stock.csv
# convert each row into a tuple
with open("stock.csv") as f:
    stock = [tuple(line) for line in csv.reader(f)]


# sql = "insert into stock (Artist, Genre, Price, Quantity, Title, Type) values (%s, %s,%s, %s, %s, %s)"


# populate stock table from stock list
sql = "insert into stock (Type, Title, Artist_Author, Genre, Quantity, Price, Discogs_GoodReadsID) values (%s, %s,%s, %s, %s, %s, %s)"
for item in stock[1:]: # i.e all tuples in stock except the header line
    # values = (tuple(list(item.values())))
    # myCursor.execute(sql, item)
    # mydb.commit()
    stockDAO.create(item)