
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
# Set up the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)
session = Session(engine)
query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

@app.route("/")
def homepage():
    print("Server returned Request for Homepage")
    return(
        f"Available Routes:<br/>"
        """
        /api/v1.0/precipitation <br/>
        /api/v1.0/stations <br/>
        /api/v1.0/tobs <br/>
        /api/v1.0/start_date and /api/v1.0/start_date/end_date <br/>
        Welcome to all the data you'll need for the dates between 2016-08-23 and 2017-08-23
        """
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_date).all()
    
    session.close()

    all_precips = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['prcp'] = prcp
        all_precips.append(precip_dict)
    
    print("Server returned request for /precipitation")
    return jsonify(all_precips)


@app.route("/api/v1.0/stations")
def stations():

    station_list = []
    results = session.query(Station.station, Station.name).all()
    session.close()
    for id, name in results:
        station_dict = {}
        station_dict['id'] = id
        station_dict['name'] = name
        station_list.append(station_dict)

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """
    Query the last 12 months of temperature observation data for station USC00519281 and return the values
    """

    results_list = []
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= query_date).\
        filter(Measurement.station == 'USC00519281').all()

    for date, temp in results:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['temp'] = temp
        results_list.append(temp_dict)
        
    return jsonify(results_list)


@app.route("/api/v1.0/")
def display():
    return(f"""TMIN, TAVG, and TMAX for a list of dates. <br/>
        <br/>
    Args: <br/>
        start_date (string): A date string in the format %Y-%m-%d <br/>
        end_date (string): A date string in the format %Y-%m-%d <br/>
         <br/>
    Returns: <br/>
        TMIN, TAVE, and TMAX <br/>
     <br/>
    Example:  <br/>
    /api/v1.0/2016-08-23/2017-08-23 - will return the values for one year
    """)


# @app.route("/api/v1.0/<start_date>/<end_date>")
# def search_by_dates(start_date, end_date='2017-08-23'):











if __name__ == '__main__':
    app.run(debug=True)