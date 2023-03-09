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

# reflecting existing database into a new model
Base = automap_base()
# reflecting the tables
Base.prepare(autoload_with=engine)

# Saving reference to the tables
Measurement = Base.classes.measurement
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
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Creating session (link) from Python to the DB
    session = Session(engine)

    """Returning dictionary of dates and precipitation values for the last 12 months"""
    # Querying for dates and precipitation values
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)


    results = session.query(Measurement.date, Measurement.prcp).\
                        filter(Measurement.date >= query_date).\
                            order_by(Measurement.date).all()

    session.close()

    # Creating a dictionary from the row data and appending to a list of precipitation values
    date_precipitation_list = []
    for date, prcp in results:
        date_precipitation_dict = {}
        date_precipitation_dict["date"] = date
        date_precipitation_dict["prcp"] = prcp
        date_precipitation_list.append(date_precipitation_dict)

    # Converting list of precipitation values to json
    return jsonify(date_precipitation_list)


@app.route("/api/v1.0/stations")
def stations():
    # Creating session (link) from Python to the DB
    session = Session(engine)

    """Returning a list of all station names"""
    # Query all stations
    results = session.query(Station.station, Station.name).all()

    session.close()

        # Creating a dictionary from the row data and appending to a list of stations
    station_list = []
    for id, name in results:
        station_dict = {}
        station_dict[id] = name
        station_list.append(station_dict)

    # Converting list stations to json
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Creating session (link) from Python to the DB
    session = Session(engine)

    """Returning dictionary of dates and temperature values for the last 12 months"""
    # Defining date for the query
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Identifiying the most active station
    station_activity = session.query(Measurement.station, func.count(Measurement.station)).\
                    group_by(Measurement.station).\
                    order_by(func.count(Measurement.station).desc()).all()
    
    # Collecting most active station id
    query_id = station_activity[0][0]

    # Using most active station ID to collect last 12 months of temperature observation data
    results = session.query(Measurement.date, Measurement.tobs).\
                        filter(Measurement.date >= query_date).\
                        filter(Measurement.station == query_id).all()

    session.close()

    # Creating a dictionary from the row data and appending to a list of temperature values
    date_temperature_list = []
    for date, tobs in results:
        date_temperature_dict = {}
        date_temperature_dict["date"] = date
        date_temperature_dict["Temperature"] = tobs
        date_temperature_list.append(date_temperature_dict)

    # Converting list of temperature values to json
    return jsonify(date_temperature_list)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Creating session (link) from Python to the DB
    session = Session(engine)

    """Returning dictionary of minimum, average and maximum temperature values since start date"""
    # Querying for temperature values
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start).all()

    session.close()

    # Creating a dictionary of the temperature values and appending to a list
    temp_list = []
    for min, avg, max in results:
        temp_dict = {}
        temp_dict['Min Temp'] = min
        temp_dict['Avg Temp'] = avg
        temp_dict['Max Temp'] = max

        temp_list.append(temp_dict)

    # Converting list of temperature values to json
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    # Creating session (link) from Python to the DB
    session = Session(engine)

    """Returning dictionary of minimum, average and maximum temperature values between start and end date"""
    # Querying for temperature values
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start).\
                    filter(Measurement.date <= end).all()

    session.close()

    # Creating a dictionary of the temperature values and appending to a list
    temp_list = []
    for min, avg, max in results:
        temp_dict = {}
        temp_dict['Min Temp'] = min
        temp_dict['Avg Temp'] = avg
        temp_dict['Max Temp'] = max

        temp_list.append(temp_dict)

    # Converting list of temperature values to json
    return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=True)