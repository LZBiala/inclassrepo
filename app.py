# Design a Flask API based on the queries that you have just developed
# Use Flask to create your routes per instructions

# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import seaborn as sns
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to Hawaii Weather Data!<br/><br/>"
        f"Routes:<br/><br/>"
        f"2016-2017 Precipitation* --------------------------------------------------  /api/v1.0/precipitation<br/><br/>"
        f"Weather Stations ------------------------------------------------------------  /api/v1.0/stations<br/><br/>"
        f"Temperature Observations* -----------------------------------------------  /api/v1.0/tobs<br/><br/>"
        f"Search Temperature Observations with Start Date** ----------------- /api/v1.0/[start]<br/><br/>"
        f"Search Temperature Observations with Start and End Date** ------ /api/v1.0/[start]/[end]<br/><br/>"
        f"*Note that 2016-2017 ranges from 08-23-2016 to 08-23-2017<br/>"
        f"**Please use YYYY-MM-DD format for start and end dates"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = last_date[0]
    
    first_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    first_date = first_date.strftime("%Y-%m-%d")

    one_yr_prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between(first_date, last_date)).all()

    prcp_list = []
    for result in one_yr_prcp:
        row = {}
        row["date"] = result[0]
        row["prcp"] = result[1]
        prcp_list.append(row)
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def weather_stations():
    stations = session.query(Station.station, Station.name).all()
    stations_list = []
    for station in stations:
        row = {}
        row["station"] = station[0]
        row["name"] = station[1]
        stations_list.append(row)
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    one_yr_tobs = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()
    tobs_list = []
    for tob in one_yr_tobs:
        row = {}
        row["date"] = tob[0]
        row["station"] = tob[1]
        row["tobs"] = tob[2]
        tobs_list.append(row)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def temp_info (start):
    start = datetime.strptime(start, "%Y-%m-%d")
    temp_queries = session.query(func.min(Measurement.tobs), func.round(func.avg(Measurement.tobs)), func.max(Measurement.tobs)).filter(Measurements.date >= start).all()
    temp_date_dict = {"TMIN": temp_queries[0][0], "TAVG": temp_queries[0][1], "TMAX": temp_queries[0][2]}
    return jsonify(temp_date_dict)

@app.route("/api/v1.0/<start>/<end>")
def temp_range_info (start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    temp_range_queries = session.query(func.min(Measurement.tobs), func.round(func.avg(Measurement.tobs)), func.max(Measurement.tobs)).filter(Measurement.date.between(start, end)).all()
    temp_date_range_dict = {"TMIN": temp_range_queries[0][0], "TAVG": temp_range_queries[0][1], "TMAX": temp_range_queries[0][2]}
    return jsonify(temp_date_range_dict)


if __name__ == "__main__":
    app.run(debug = True)