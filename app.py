###################################################
# Python SQL toolkit and Object Relational Mapper #
###################################################
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc
from flask import Flask, jsonify
import pandas as pd

##################################
# create engine to hawaii.sqlite #
##################################
import os
os.chdir("Resources")
engine = create_engine("sqlite:///hawaii.sqlite")
os.chdir("..")
#################################################
# reflect an existing database into a new model #
#################################################
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
#################################
# Save references to each table #
#################################
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)


@app.route("/")
def home():
    return (
        # space key : &nbsp;
        # '<' key   : &lt;
        # '>' key   : &gt;
        f'Welcome to My Climate API Service<br/><br/>'
        f'Available Routes:<br/>'
        f'{"&nbsp;"*6}/api/v1.0/precipitation<br/>'
        f'{"&nbsp;"*12}Receive date and precipitation values recorded in JSON format.<br/>'
        f'{"&nbsp;"*6}/api/v1.0/stations<br/>'
        f'{"&nbsp;"*12}Receive information about the recording stations in JSON format.<br/>'
        f'{"&nbsp;"*6}/api/v1.0/tobs<br/>'
        f'{"&nbsp;"*12}Receive temperature data from the most active recording station in '
            f' JSON format.<br/>'
        f'{"&nbsp;"*6}/api/v1.0/&lt;start&gt;<br/>'
        f'{"&nbsp;"*12}Replace &lt;start&gt; with a date in yyyy-mm-dd<br/>'
        f'{"&nbsp;"*12}Receive Minimum, Highest, and Average temperatures starting at the date you entered '
            f'in a JSON format.<br/>'
        f'{"&nbsp;"*6}/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>'
        f'{"&nbsp;"*12}Replace &lt;end&gt; with a date in yyyy-mm-dd<br/>'
        f'{"&nbsp;" * 12}Receive Minimum, Highest, and Average temperatures starting at the date you entered '
            f'up to the end date in JSON format. <br/>'
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    ###########################
    # Establish/close session #
    ###########################
    session = Session(engine)
    data = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    ###############################
    # Create the JSON information #
    ###############################
    json_data = []
    for date, prcp in data:
        new_dict = {"date": date, "prcp": prcp}
        json_data.append(new_dict)
    return jsonify(json_data)  # Return all of the dates/prcp data in JSON


@app.route("/api/v1.0/stations")
def stations():
    ###########################
    # Establish/close session #
    ###########################
    session = Session(engine)
    data = session.query(Station.name, Station.longitude, Station.latitude, Station.elevation).all()
    session.close()

    ###############################
    # Create the JSON information #
    ###############################
    json_data = []
    for name, longitude, latitude, elevation in data:
        new_dict = {"name": name, "longitude": longitude, "latitude": latitude, "elevation": elevation}
        json_data.append(new_dict)
    return jsonify(json_data)  # Return all of the Station data in JSON


@app.route("/api/v1.0/tobs")
def tobs():
    ###########################
    # Establish/close session #
    ###########################
    session = Session(engine)
    data = session.query(Station.name, Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').where(
        Station.id == 7).all()
    session.close()

    ###############################
    # Create the JSON information #
    ###############################
    json_data = []
    for name, date, tobs in data:
        new_dict = {"name": name, "date": date, "temperature": tobs}
        json_data.append(new_dict)
    return jsonify(json_data)


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
