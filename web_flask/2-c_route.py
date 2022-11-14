#!/usr/bin/python3
""" The 2-c_route.py module: defines flask usage """

from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """ displays hello at the root endpoint """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ returns HBNB """
    return "HBNB"


@app.route('/c/<text>')
def c_route(text):
    "returns C with the value of the text variable"
    return "C {}".format(text.replace("_", " "))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
