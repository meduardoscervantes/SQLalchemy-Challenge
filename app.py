###################################################
# Python SQL toolkit and Object Relational Mapper #
###################################################
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    # Todo: List all the routes available
    return "Welcome to my 'Home' page!"


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Todo:Convert the query results to a dictionary using
    #   date as the key and prcp as the value.
    return "Welcome to my 'About' page!"


@app.route("/api/v1.0/stations")
def stations():
    # Todo:Return a JSON list of stations from the dataset.
    return "Welcome to my 'About' page!"


@app.route("/api/v1.0/tobs")
def tobs():
    # Todo:Query the dates and temperature observations
    #   of the most active station for the last year of data.
    #   Return a JSON list of temperature observations (TOBS) for the previous year.
    return "Welcome to my 'About' page!"


@app.route("/api/v1.0/<start>")
def start_temp():
    # Todo:Return a JSON list of the minimum temperature, the average temperature,
    #   and the max temperature for a given start or start-end range.
    return "Welcome to my 'About' page!"


@app.route("/api/v1.0/<start>/<end>")
def range_temp():
    # Todo:Return a JSON list of the minimum temperature, the average temperature,
    #   and the max temperature for a given start or start-end range.
    return "Welcome to my 'About' page!"


if __name__ == "__main__":
    app.run(debug=True)
