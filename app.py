
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

    session = Session(engine)

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_date).all()
    
    session.close()

    all_precips = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['prcp'] = prcp
        all_precips.append(precip_dict)
    
    return jsonify(all_precips)


# @app.route("/api/v1.0/stations")


# @app.route("/api/v1.0/tobs")


# @app.route()









if __name__ == '__main__':
    app.run(debug=True)