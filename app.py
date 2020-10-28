# Import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt


# DB Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Refrences
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask
app = Flask(__name__)


# Routes for flask

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;` and `/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
        f"dates must be written as YYYY-MM-DD"
    )

# All the routes 
@app.route("/api/v1.0/precipitation")
def precipitaion():
    #open the session
    session = Session(engine)
    
    results = session.query(Measurement.date, Measurement.prcp, Measurement.station).all()
    
    session.close()
    
    all_precipitation = []
    for date, prcp, station in results:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        precipitation_dict['station'] = station
        all_precipitation.append(precipitation_dict)
        
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    
    all_station = list(np.ravel(results))
    
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    results = session.query(Measurement.date, Measurement.tobs, Measurement.station)\
                        .filter(and_(Measurement.date>=startDate, Measurement.date<=endDate))\
                        .all()
    
    session.close()
    
    all_temps = []
    for date, tobs, station in results:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['tobs'] = tobs
        temp_dict['station'] = station
        all_temps.append(temp_dict)
    
    return jsonify(all_temps)

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    
    session = Session(engine)
    
    results = session.query(Measurement.date, \
                         func.avg(Measurement.tobs), func.min(Measurement.tobs), func.max(Measurement.tobs))\
                        .filter(Measurement.date>=start_date)\
                        .group_by(Measurement.date)\
                        .all()
    
    session.close()
    
    dates = []
    for result in results:
        date_dict = {}
        date_dict['date'] = result[0]
        date_dict['avg temp'] = result[1]
        date_dict['min temp'] = result[2]
        date_dict['max temp'] = result[3]
        dates.append(date_dict)
    
    return jsonify(dates)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date,end_date):
    session = Session(engine)
    
    results = session.query(Measurement.date, \
                         func.avg(Measurement.tobs), func.min(Measurement.tobs), func.max(Measurement.tobs))\
                        .filter(and_(Measurement.date>=start_date,Measurement.date<=end_date))\
                        .group_by(Measurement.date)\
                        .all()
    
    session.close()
    
    dates = []
    for result in results:
        date_dict = {}
        date_dict['date'] = result[0]
        date_dict['avg temp'] = result[1]
        date_dict['min temp'] = result[2]
        date_dict['max temp'] = result[3]
        dates.append(date_dict)
    
    return jsonify(dates)

# Main behavior/debug
if __name__ == "__main__":
    app.run(debug=True)