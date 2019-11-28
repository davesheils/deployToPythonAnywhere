#!flask/bin/python

from flask import Flask
from flask_cors import CORS
# line of code not in lab sheet
# used to define app
# see following for solution:
# https://stackoverflow.com/questions/29277581/flask-nameerror-name-app-is-not-defined

app = Flask(__name__, static_url_path='',static_folder = '.')
# app.config.from_object('config')
CORS(app)

@app.route('/')
def index():
    return "<i>Hello, World!</i>"

@app.route('/book/<int:id>')

def getBook(id):
    return "You want book with " + str(id)



@app.route('/album/<string:title>')

def getAlbum(title):
    return "You want " + title



if __name__ == '__main__' :
    app.run(debug = True)