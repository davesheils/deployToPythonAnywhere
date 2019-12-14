#!flask/bin/python

# Code based on lecture DR8.2 REST

# Building a simple rest server

from flask import Flask, jsonify, request, abort, make_response, render_template
import json
from StockDAO import stockDAO

# from flask_cors import CORS # review if this is necessary

app = Flask(__name__, static_url_path='',static_folder = '.')

@app.route('/')
def home():
    # return "<i>Hello, Customers!</i>"
    return render_template("home.html")

# CRUD Methods

# READ with ['GET']
@app.route('/stock', methods=['GET'])
def getAll():
    stock = stockDAO.getAll()
    return jsonify(stock) #jsonify comes from flask. compare with week 5, w
# curl -i http://localhost:5000/stock

# Find stock item by ID
@app.route('/stock/<int:id>',  methods =['GET', 'POST', 'PUT'])
def findByID(id):
    foundItem =stockDAO.getByID(id)
    return jsonify(foundItem)
#    curl -i http://127.0.0.1:5000/stock/5
    
# CREATE with ['POST']
@app.route('/stock', methods = ['POST'])
def create():
    if not request.json:
        abort(400)
    # item = {"Type":request.json['Type'],
    #        "Title":request.json['Title'],
    #        "Artist_Author":request.json['Artist_Author'],
    #        "Genre":request.json['Genre'],
    #        "Quantity":request.json['Quantity'],
    #        "Price":request.json['Price']
    #        # "Discogs_GoodReadsID":request.json['Discogs_GoodReadsID'],
    #        }
    # values = (item['Type'],item['Title'],item['Artist_Author'],item['Genre'],item['Quantity'],item['Price'])
    item = request.json
    values = tuple(list(item.values()))
    newID = stockDAO.create(values)
    item['id'] = newID
    return jsonify(item)

    
    
# UPDATE with ['PUT']
@app.route('/stock/<int:id>', methods = ['PUT'])
def update(id):
    foundItem = stockDAO.getByID(id)
    if not foundItem:
        abort(404)
    if not request.json:
        abort(400)    
    reqJSON = request.json
    if 'Type' in reqJSON: # and type(reqJSON['Type']) is str:
        foundItem['Type'] = reqJSON['Type']
    if 'Title' in reqJSON: # and type(reqJSON['Title']) is str:
        foundItem['Title'] = reqJSON['Title']
    if 'Artist_Author' in reqJSON: # and type(reqJSON['Artist_Author']) is str:
        foundItem['Artist_Author'] = reqJSON['Artist_Author']
    if 'Genre' in reqJSON: # and type(reqJSON['Genre']) is str:
        foundItem['Genre'] = reqJSON['Genre']
    if 'Quantity' in reqJSON: # and type(reqJSON['Quantity']) is int:
        foundItem['Quantity'] = reqJSON['Quantity']    
    if 'Price' in reqJSON: # and type(reqJSON['Price']) is float:
        foundItem['Price'] = reqJSON['Price']
    if 'Discogs_GoodReadsID' in reqJSON: # and type(reqJSON['Discogs_GoodReadsID']) is str:
        foundItem['Discogs_GoodReadsID'] = reqJSON['Discogs_GoodReadsID']
    values = (foundItem['Type'],foundItem['Title'],foundItem['Artist_Author'],foundItem['Genre'],foundItem['Quantity'],foundItem['Price'],foundItem['Discogs_GoodReadsID'], foundItem['id'])
    stockDAO.update(values)
    return jsonify(foundItem)


# DELETE with ['DELETE']
@app.route('/stock/<int:id>', methods = ['DELETE'])
def delete(id):
    stockDAO.delete(id)
    return jsonify( {'result':'true'})
    # example of delete with curl
    # curl -X DELETE http://davidsheils.pythonanywhere.com/stock/2

if __name__ == '__main__' :
    app.run(debug= True)