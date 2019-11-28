#!flask/bin/python

from flask import Flask

app = Flask(__name__, static_url_path='',static_folder = '.')

@app.route('/')
def index():
    return "<i>Greetings, Earthlings </i>"

@app.route('/book/<int:id>')

def getBook(id):
    return "You want book with " + str(id)



@app.route('/album/<string:title>')

def getAlbum(title):
    return "You want " + title



if __name__ == '__main__' :
    app.run(debug = True)