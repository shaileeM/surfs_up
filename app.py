import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#setup database engine for the flask application 
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

#get both the tables in the following variables
Measurement = Base.classes.measurement
Station = Base.classes.station

#create a session link from python to database
session = Session(engine)

#following will create flask application called "app"
app = Flask(__name__)

#define the starting point, also known as the root
@app.route("/")

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
    
#create precipitation route
@app.route("/api/v1.0/precipitation")

def precipitation():
    prev_year= dt.date(2017,8,23)- dt.timedelta(days=365)
    precipitation = session.query(Measurement.date,Measurement.prcp).\
                    filter(Measurement.date>=prev_year).all()
    #create dictionary with date as key and precipitaion as value
    precip={date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#create station route(return list of all the stations)
@app.route("/api/v1.0/stations")

def stations():
    results=session.query(Station.station).all()
    #now unravel the result into 1d array
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#create temperature route
@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #query the primary station for all the temp obv from the prev year
    results= session.query(Measurement.tobs).filter(Measurement.station=='USC00519281').\
                                             filter(Measurement.date>=prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#statistics route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
    