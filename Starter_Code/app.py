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
engine = create_engine("sqlite:///hawaii.sqlite")



# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

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
        f"Temperature record: /api/v1.0/tobs<br/>"
        f"Temperature from a date entered to current date (enter in yyy-mm-dd format): /api/v1.0/yyyy-mm-dd>"
        f"Temperature from a range of dates (enter in yyy-mm-dd format, earliest first follow by latest): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd>
        


@app.route("/api/v1.0/***")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Passenger.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)