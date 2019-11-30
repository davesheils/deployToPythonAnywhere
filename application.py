#!flask/bin/python

# Code based on lecture DR8.2 REST

# Building a simple rest server


from flask import Flask, jsonify,  request, abort, make_response
import json

# from flask_cors import CORS # review if this is necessary

app = Flask(__name__, static_url_path='',static_folder = '.')

# create python list of JSON objects 

stock = [
    {"id":1,"Type":"Book","Title":"Starve Acre","Artist":"Andrew Michael Hurley","Genre":"Horror","Quantity":25,"Price":15.99},
    {"id":2,"Type":"CD","Title":"Path: An Ambient Journey from Windham Hill","Artist":"Various Artists","Genre":"Ambient/New Age","Quantity":10,"Price":4.95},
    {"id":3,"Type":"CD","Title":"The Freewheelin' Bob Dylan","Artist":"Bob Dylan","Genre":"Folk/Folk-Rock","Quantity":30,"Price":9.99},
    {"id":4,"Type":"Book","Title":"The Milkman","Artist":"Anna Burns","Genre":"Literature","Quantity":12,"Price":8.99},
    {"id":5,"Type":"Vinyl LP","Title":"Mark Hollis","Artist":"Mark Hollis","Genre":"Alternative","Quantity":5,"Price":24.99}
]

# ID to keep track of cars. Will be incremented when stock items are added
nextID  = 6

@app.route('/')
def index():
    return "<i>Hello, Customers!</i>"


# CRUD Methods

# READ with ['GET']
@app.route('/stock', methods=['GET'])
def getAll():
    return jsonify(stock) #jsonify comes from flask. compare with week 5, w
# curl -i http://localhost:5000/stock


# Find stock item by ID
@app.route('/stock/<int:id>')
def findByID(id):
    foundItem = list(filter(lambda s : s['id'] == id , stock))
    if len(foundItem) == 0:
        return jsonify( {} ),204 
    return jsonify( { 'id' : foundItem[0] })
#    curl -i http://127.0.0.1:5000/stock/5
    


# CREATE with ['POST']
@app.route('/stock', methods = ['POST'])
def create():
    global nextID
    if not request.json:
        abort(400)
    # add code to check if correctly formatted
    # i.e correct datatypes, all mandatory fields filled in ...
    stockItem = {
        "id": nextID,
        "Type": request.json['Type'],
        "Title": request.json['Title'],
        "Artist":request.json['Artist'],
        "Genre":request.json['Genre'],
        "Quantity":request.json['Quantity'],
        "Price":request.json['Price']
    }
    stock.append(stockItem)
    nextID += 1
    # newItem = json.dumps(stockItem)
    # return newItem,201
    return jsonify(stockItem),201
    # return "Post nextID = " + str(nextID)
    # curl -i -H  "Content-Type:application/json" -X POST -d '{"Type":"LP","Title":"In the Land of Grey and Pink","Artist":"Caravan","Genre":"Progressive/Jazz Rock","Quantity":7,"Price":24.99}' http://davidsheils.pythonanywhere.com/stock


# UPDATE with ['PUT']
@app.route('/stock/<int:id>', methods = ['PUT'])
def update(id):
    # find item to update ...
    foundItems = list(filter(lambda s : s['id'] == id , stock))
    if len(foundItems) == 0: # no book found
        abort(404)

    # week 08 code:
    foundItem = foundItems[0]
    if not request.json:
        abort(400)    
    reqJSON = request.json
    # week 08 code to update item, added validation of datatypes (as per week 05):
    if 'Artist' in reqJSON and type(reqJSON['Artist']) is str:
        foundItem['Artist'] = reqJSON['Artist']
    if 'Genre' in reqJSON and type(reqJSON['Genre']) is str:
        foundItem['Genre'] = reqJSON['Genre']
    if 'Price' in reqJSON and type(reqJSON['Price']) is float:
        foundItem['Price'] = reqJSON['Price']
    if 'Quantity' in reqJSON and type(reqJSON['Quantity']) is int:
        foundItem['Quantity'] = reqJSON['Quantity']
    if 'Title' in reqJSON and type(reqJSON['Title']) is str:
        foundItem['Title'] = reqJSON['Title']
    if 'Type' in reqJSON and type(reqJSON['Type']) is str:
        foundItem['Type'] = reqJSON['Type']
    return jsonify(foundItem)
    # Updating with curl
    # curl -i -H  "Content-Type:application/json" -X PUT -d '{"Genre":"Alternative/Punk"}' http://davidsheils.pythonanywhere.com/stock/6

# DELETE with ['DELETE']
@app.route('/stock/<int:id>', methods = ['DELETE'])
def delete(id):
    foundItems = list(filter(lambda s : s['id'] == id , stock))
    if len(foundItems) == 0:
        abort(404)
    stock.remove(foundItems[0])
    return jsonify( {'result':'true'})
    # example of delete with curl
    # curl -X DELETE http://davidsheils.pythonanywhere.com/stock/2

if __name__ == '__main__' :
    app.run(debug= True)