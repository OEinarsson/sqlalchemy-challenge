# Import the dependencies.

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")



# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
site = Base.classes.station

# Create our session (link) from Python to the DB


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
        f"precipitation: /api/v1.0/precipitation<br/>"
        f"list of station: /api/v1.0/stations<br/>"
        f"Temperature records from most active station: /api/v1.0/tobs<br/>"
        f"Temperature from a date entered to current date (enter in yyy-mm-dd format): /api/v1.0/yyyy-mm-dd><br/>"
        f"Temperature from a range of dates (enter in yyy-mm-dd format, earliest first follow by latest): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    recent_date = dt.datetime.strptime(recent_date, '%Y-%m-%d')
    date = dt.date(recent_date.year -1, recent_date.month, recent_date.day)
    result = session.query(measurement.date,measurement.prcp).filter(measurement.date >= date).all()
    session.close()

    precipitation = []
    for date, prcp in result:
        perc_dict = {}
        perc_dict["Date"] = date
        perc_dict["Precipitation"] = prcp
        precipitation.append(perc_dict)

    return jsonify(precipitation)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    result = session.query(site.station,site.name,site.latitude,site.longitude,site.elevation).all()
    session.close()

    station_data = []
    for station,name,lat,lon,el in result:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = el
        station_data.append(station_dict)

    return jsonify(station_data)

@app.route('/api/v1.0/tobs')
def top_station_results():
    session = Session(engine)

    top_station = session.query(measurement.station,func.count(measurement.id)).\
    group_by(measurement.station).\
    order_by(func.count(measurement.id).desc()).first()

    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    recent_date = dt.datetime.strptime(recent_date, '%Y-%m-%d')
    date = dt.date(recent_date.year -1, recent_date.month, recent_date.day)

    result = session.query(measurement.date,measurement.tobs).filter(measurement.station == top_station[0]).filter(measurement.date >= date).all()
    session.close()

    station_results = []
    for date, tobs in result:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        station_results.append(tobs_dict)

    return jsonify(station_results)

@app.route('/api/v1.0/<start>')
def selected_start(start):
    session = Session(engine)
    result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    session.close()

    tobs = []
    for min,avg,max in result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs.append(tobs_dict)

    return jsonify(tobs)

@app.route('/api/v1.0/<start>/<stop>')
def selected_range(start,stop):
    session = Session(engine)
    result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= stop).all()
    session.close()

    tobs = []
    for min,avg,max in result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs.append(tobs_dict)


    return jsonify(tobs)
if __name__ == '__main__':
    app.run(debug=True)