#!flask/bin/python

# Code based on lecture DR8.2 REST

# Building a simple rest server

from flask import Flask, jsonify, request, abort, make_response, render_template
import json

stock = [
    {
        "id":1,
        "Type":"Book",
        "Title":"Book 1",
        "Artist_Author":"Author 1",
        "Genre":"Fiction",
        "Quantity":"10",
        "Price":10,
        "Discogs_GoodReadsID":"12345"
    },
    {
        "id":2,
        "Type":"CD",
        "Title":"CD 1",
        "Artist_Author":"Band 1",
        "Genre":"Punk Rockers",
        "Quantity":"10",
        "Price":11,
        "Discogs_GoodReadsID":"678910"
    },
    {
        "id":3,
        "Type":"LP",
        "Title":"LP 1",
        "Artist_Author":"Band 1",
        "Genre":"Roots Rockers",
        "Quantity":"10",
        "Price":12,
        "Discogs_GoodReadsID":"234354"
    }]

nextID = 4

app = Flask(__name__, static_url_path='',static_folder = '.')

@app.route('/')
def home():
    # return "<i>Hello, Customers!</i>"
    return render_template("home.html")

# CRUD Methods

# READ with ['GET']
@app.route('/stock', methods=['GET'])
def getAll():
    ##  stock = stockDAO.getAll()
    return jsonify(stock) #jsonify comes from flask. compare with week 5, w
# curl -i http://localhost:5000/stock

# Find stock item by ID
@app.route('/stock/<int:id>', methods =['GET', 'POST', 'PUT'])
def findByID(id):
    foundItem = list(filter(lambda t : t['id'] == id , stock))
    if len(foundItem) == 0:
        return jsonify( { 'stock' : '' }),204
    return jsonify( { 'stock' : foundItem[0] })
#    curl -i http://127.0.0.1:5000/stock/5
    
# CREATE with ['POST']
@app.route('/stock', methods = ['POST'])
def create():
    global nextID
    if not request.json:
        abort(400)
    item = {"Type":request.json['Type'],
           "Title":request.json['Title'],
            "Artist_Author":request.json['Artist_Author'],
            "Genre":request.json['Genre'],
            "Quantity":request.json['Quantity'],
            "Price":request.json['Price'],
            "Discogs_GoodReadsID":request.json['Discogs_GoodReadsID']
            }
    item["id"] = nextID
    nextID += 1
    return jsonify(item)

    
    
# UPDATE with ['PUT']
@app.route('/stock/<int:id>', methods = ['PUT'])
def update(id):
    foundItem = list(filter(lambda t : t['id'] == id , stock))
    if len(foundItem) == 0:
        return jsonify( { 'stock' : '' }),204
    
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
        
    # values = tuple(list(foundItem.values())) # not sure why this does not work here ...
     
    # stockDAO.update(values)nextID
    return jsonify(foundItem)


# DELETE with ['DELETE']
@app.route('/stock/<int:id>', methods = ['DELETE'])
def delete(id):
    stock.delete(id)
    return jsonify( {'result':'true'})
    # example of delete with curl
    # curl -X DELETE http://davidsheils.pythonanywhere.com/stock/2

if __name__ == '__main__' :
    app.run(debug= True)