""" the 8-cities_by_states.py module """
from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exc):
    """ release sqlalchemy session """
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def c_by_s_route():
    """ displays cities linked with states """
    states = storage.all("State")
    return render_template("8-cities_by_states.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
