from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    # Todo: List all the routes available
    return "Welcome to my 'Home' page!"


@app.route("/api/v1.0/precipitation")
def about():
    # Todo:Convert the query results to a dictionary using
    #   date as the key and prcp as the value.
    return "Welcome to my 'About' page!"


@app.route("/api/v1.0/stations")
def about():
    # Todo:Return a JSON list of stations from the dataset.
    return "Welcome to my 'About' page!"


@app.route("/api/v1.0/tobs")
def about():
    # Todo:Query the dates and temperature observations
    #   of the most active station for the last year of data.
    #   Return a JSON list of temperature observations (TOBS) for the previous year.
    return "Welcome to my 'About' page!"


@app.route("/api/v1.0/<start>")
def about():
    # Todo:Return a JSON list of the minimum temperature, the average temperature,
    #   and the max temperature for a given start or start-end range.
    return "Welcome to my 'About' page!"


@app.route("/api/v1.0/<start>/<end>")
def about():
    # Todo:Return a JSON list of the minimum temperature, the average temperature,
    #   and the max temperature for a given start or start-end range.
    return "Welcome to my 'About' page!"


if __name__ == "__main__":
    app.run(debug=True)
