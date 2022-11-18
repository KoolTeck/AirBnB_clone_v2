#!/usr/bin/python3
""" The 7-states_list.py module: defines flask usage """

from flask import Flask, render_template
from models import storage

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


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text='is cool'):
    """ returns Python with the value of the var """
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def num_route(n):
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def num_temp_route(n):
    """ return html template when endpoint is requested """
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def odd_even_route(n):
    """ return template with odd or even value """
    value = "even" if n % 2 == 0 else "odd"
    return render_template('6-number_odd_or_even.html', n=n, value=value)


@app.route('/states_list', strict_slashes=False)
def states_route():
    """ displays list of states """
    all_states = storage.all("State")
    return render_template("7-states_list.html", all_states=all_states)


@app.teardown_appcontext
def teardown_db(exception):
    """ frees the db session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
