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
    data = session.query(Station.name, Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23')\
        .where(Station.id == 7).all()
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
def start_temp(start):
    ##########################################################
    # Check to see if the date exists and proceed from there #
    ##########################################################
    session = Session(engine)
    df = pd.DataFrame(session.query(Measurement.date))
    df.columns = ["date"]
    if start in df["date"].tolist():
        data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
            .filter(Measurement.date >= start).all()
        session.close()
        json_data = []
        for x, y, z in data:
            new_dict = {"units": "fahrenheit", "min": x, "avg": y, "max": z}
            json_data.append(new_dict)
        return jsonify(json_data)
    session.close()
    return jsonify({"error": f"Date: {start} not found."}), 404


@app.route("/api/v1.0/<start>/<end>")
def range_temp(start, end):
    ##########################################################
    # Check to see if the date exists and proceed from there #
    ##########################################################
    session = Session(engine)
    df = pd.DataFrame(session.query(Measurement.date))
    df.columns = ["date"]

    if start not in df["date"].tolist():  # Check if the start date exists
        session.close()
        return jsonify({"error": f"Start date: {start} not found."}), 404

    if end not in df["date"].tolist():  # Check if the end date exists
        session.close()
        return jsonify({"error": f"End date: {end} not found."}), 404

    if start > end:  # Ensure the start date comes before the end date.
        session.close()
        return jsonify({"error": f"Not correct start/end format... Make sure the start date is before end date"}), 404

    if start in df["date"].tolist() and end in df["date"].tolist():  # Ensure the date exists in the DB
        data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)) \
            .filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        session.close()
        json_data = []
        for x, y, z in data:
            new_dict = {"units": "fahrenheit", "min": x, "avg": y, "max": z}
            json_data.append(new_dict)
        session.close()
        return jsonify(json_data)


if __name__ == "__main__":
    app.run(debug=True)
