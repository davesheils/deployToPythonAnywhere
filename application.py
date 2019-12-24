#!flask/bin/python

# Code based on lecture DR8.2 REST

# Building a simple rest server

from flask import Flask, flash, session, url_for, redirect, jsonify, request, abort, make_response, render_template
import secrets
import json
from StockDAO import stockDAO
# import discogs and wikipedia python clients
import discogs_client
import wikipedia

# from flask_cors import CORS # review if this is necessary

app = Flask(__name__, static_url_path='',static_folder = '.')

# Login simulation
# htps://pythonise.com/series/learning-flask/flask-session-object
# secrets.token_urlsafe(16)
app.secret_key = "ABCDEFG12345678"

users = [
        {"username":"admin","password":"pass1"},
        {"username":"davesheils","password":"pass2"},
        {"username":"andrewbeatty","password":"pass3"}
        ]


@app.route('/')
def home():
    if not 'username' in session:
        return redirect(url_for("login"))
    else:
        return render_template("home.html", user = session['username'])

@app.route('/moreinfo/<int:id>')
def moreInfo(id):
    d = discogs_client.Client('davesApp/0.1')
    release = d.release(id)
    # This needs to be tweaked to ensure correct album summary is returned
    title = release.title + " (Album)"
    #  get artist .. bit of parsing required here as artist object is a list
    artist = str(release.artists[0]).split("'")[1]
    genres = release.genres 
    summary = wikipedia.page(title).summary
    # create tracklist
    tracklist = release.tracklist
    return render_template("moreinfo.html", title = title, artist = artist, genres = genres, summary = summary, tracklist = tracklist, user = session['username'])


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    # return render_template("logout.html")
    session.pop('username', None)
    return render_template("logout.html") 

@app.route('/sign-in', methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        req = request.form 
        username = req.get("username")
        password = req.get("password")
        # require for loop to get list of users and validate
        for user in users:
            if username == user["username"] and password == user["password"]:
                session["username"] = username
                flash("You are logged in")
                return redirect(url_for("home"))
        else:
            flash("User credentials not valid. Returning you to login screen")
            return redirect(url_for("login"))
# CRUD Methods

# READ with ['GET']
@app.route('/stock', methods=['GET'])
def getAll():
    stock = stockDAO.getAll()
    return jsonify(stock) #jsonify comes from flask. compare with week 5, w
# curl -i http://localhost:5000/stock

# Find stock item by ID
@app.route('/stock/<int:id>',  methods =['GET'])
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
def update_item(id):
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