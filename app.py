import os
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect



# Find the most recent date in the data set from measurement table
from datetime import datetime

# Import Flask
from flask import Flask, jsonify

##################################
#DATABASE SETUP
###################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

base =automap_base()
base.prepare(engine, reflect=True)

station = base.classes.station
measurement = base.classes.measurement
######################################
#FLASK SETUP
######################################

app = Flask(__name__)

###################################
# FLASK ROUTES
###################################

@app.route("/")
def welcome():
    return (
        f"AVAILABLE ROUTES:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/end<start><end><br/>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    ##Create a Session (from python to the DB)##
    session = Session(engine)
    ##Query Data##
    recent_data = session.query(measurement.date,measurement.prcp).filter(measurement.date>='2016-08-23').all()
    
    session.close()


    ##Create a dictionary from the row data and append to a list##
    all_prcp = []
    for date, prcp in recent_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)
        
    return jsonify(all_prcp)



@app.route("/api/v1.0/stations")
def stations():
    ##Create a Session (from python to the DB)##
    session = Session(engine)
    ##Query Data##
    station_data = session.query(station.station,station.name).all()
    
    session.close() 

    ###Convert tuples list to normal list##
    all_stations = list(np.ravel(station_data))
    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def tobs():

    ##Create a Session (from python to the DB)##
    session = Session(engine)
    ##Query Data##
    temp_data=session.query(measurement.date,measurement.tobs).filter(measurement.date>='2016-08-23').\
    filter(measurement.station=='USC00519281').all()
    
    session.close()

    ##Create a dictionary from the row data and append to a list##
    all_temp = []
    for date, tobs in temp_data:
       temp_dict = {}
       temp_dict["date"] = date
       temp_dict["tobs"] = tobs
       all_temp.append(temp_dict)   

    return jsonify(all_temp)

    
@app.route("/api/v1.0/<start>")
def start_date(start):
    ##Create a Session (from python to the DB)##
    session = Session(engine)
    ##Query Data##
    start_tobs_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()

    session.close()

    ##Create a dictionary from the row data and append to a list##
    start_temps = []
    for min,avg,max in start_tobs_data:
        start_temp_dict = {}
        start_temp_dict["min_temp."] = min
        start_temp_dict["avg_temp."] = avg
        start_temp_dict["max_temp."] = max
        start_temps.append(start_temp_dict)

    return jsonify(start_temps)



@app.route("/api/v1.0/<start>/<end>")
def start_end_dates(start,end):
    ##Create a Session (from python to the DB)##
    session = Session(engine)
    ##Query Data##
    end_tobs_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()

    session.close()

    ##Create a dictionary from the row data and append to a list##
    end_temps = []
    for min,avg,max in end_tobs_data:
        end_temp_dict = {}
        end_temp_dict["min_temp"] = min
        end_temp_dict["avg_temp"] = avg
        end_temp_dict["max_temp"] = max
        end_temps.append(end_temp_dict)

    return jsonify(end_temps)



if __name__ == "__main__":
    app.run(debug=True)