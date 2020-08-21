import numpy as np
import pandas as pd
import sqlalchemy
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.Measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurements.date, Measurements.prcp)
    
    session.close()

    rain_data = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        rain_data.append(prcp_dict)
    return jsonify(rain_data)
    
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Measurements.station)
    
    session.close()

    data = []

    for station in results:
        station_dict = {}
        station_dict["station"] = station
        data.append(station_dict)
    return jsonify(data)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.station, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.station == 'USC00519281').\
    group_by(Measurement.station).first()
    
    session.close()
    
    tobs = []

    for date, tobs, station in results:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs.append(tobs_dict)
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()
    
    session.close()
    
    original_list = []

    for min, avg, max in sel:
        date_dict = {}
        date_dict["min temp"] = min
        date_dict["avg temp"] = avg
        date_dict["max temp"] = max
        original_list.append(date_dict)
    return jsonify(original_list)

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    session = Session(engine)
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()
    
    session.close()
    
    last_list = []

    for min, avg, max in sel:
        date_dict = {}
        date_dict["min temp"] = min
        date_dict["avg temp"] = avg
        date_dict["max temp"] = max
        last_list.append(date_dict)
    return jsonify(last_list)

if __name__ == '__main__':
    app.run(debug=True)