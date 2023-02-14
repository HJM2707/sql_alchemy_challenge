# importing the required libraries
import pandas as pd
#import numpy
import numpy as np
#import datetime
import datetime as dt
#importing date and timedelta
from datetime import date, timedelta
#importing sqlalchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
# engine creation to analysing data from SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


#reflect the existing database into new model
Base = automap_base()
#reflect the tables in the database
Base.prepare(engine, reflect=True)
#referencing the table
Measure = Base.classes.measurement
Station = Base.classes.station
# Flask initializing
app = Flask(__name__)



# Define the home route
@app.route("/")
def home():
    print("Return a message with a list of available API routes")
    return (f"<h1>Hawaii climates data are available in following API's</h1>"
            f"<h3>The API routes are:</h2>"
            f"<b>For precipitation</b>:        /api/v1.0/precipitation<br/>"
            f"<b>Stations</b>:     /api/v1.0/stations<br/>"
            f"<b>Temperature data for most active station for 1 Year </b>:    /api/v1.0/tobs"
            f"<h4>Please choose the start and end date in the following manner: For the following links please enter <em>start</em> and <em>end</em> dates as YYYY-MM-DD  -  <em>(available dates are 2010-01-01 and 2017-08-23)</em></h4>"
            f"<b>For Min, Avg and Max Temperature observed for all dates from chosen date, please follow that </b>:/api/v1.0/<em><b>start</b></em><br/>"
            f"<b>For Min, Avg and Max Temperature observed for start and end choose as it is</b>: /api/v1.0/<em><b>start</b></em>/<em><b>end</b></em>")

# Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Retrieve the last 12 months of precipitation data."""
    # Create a session from Python to the Database
    session = Session(engine)
    # Query the date column of the Measurement table for the most recent date
    recent_date = session.query(Measure.date).order_by(Measure.date.desc()).first()
    
    # Convert the most recent date string to a date object
    recent_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    # Calculate the date one year prior to the most recent date
    year_ago = recent_date - dt.timedelta(days=365)
    
    # Query the date and prcp columns of the Measurement table for data from the past year
    precipitation = session.query(Measure.date, Measure.prcp).\
        filter(Measure.date >= year_ago).\
        order_by(Measure.date).all()
    
    # Convert the query results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation}
    
    # Return the dictionary as JSON data
    return jsonify(precipitation_dict)

# Define the station route
@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    # Create a session from Python to the Database
    session = Session(engine)
    # Query the station table to retrieve the name and station columns
    result = session.query(Station.name, Station.station).all()
    
    # Convert the result of the query into a list of dictionaries
    stations = [{"name": row[0], "station": row[1]} for row in result]
    
    # Return the list of dictionaries as a JSON object
    return jsonify(stations)

# Define the tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    """Dates and temperature observations from a year from the last data point for the most active station."""
    # Create a session from Python to the Database
    session = Session(engine)
    # Query the most active station from the measurement table
    most_active_station = session.query(Measure.station, func.count(Measure.station)).\
                                  group_by(Measure.station).\
                                  order_by(func.count(Measure.station).desc()).first()[0]
    # Find the most recent date for the most active station
    recent_date = session.query(Measure.date).\
                            filter(Measure.station == most_active_station).\
                            order_by(Measure.date.desc()).first()[0]
    # Calculate the date one year prior to the recent date
    one_year_ago = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    # Query tobs data for the previous year from the most active station
    tobs_data = session.query(Measure.date, Measure.tobs).\
                           filter(Measure.date >= one_year_ago).\
                           filter(Measure.station == most_active_station).\
                           order_by(Measure.date).all()
    # Convert the tobs query results to a dictionary and return it as JSON
    tobs_list = []
    for date, tobs in tobs_data:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

# Define Start date temperature route
@app.route("/api/v1.0/<start>")
def start_date(start):
    """Return a JSON list of the MIN, AVG and MAX temperatures from a given date range."""
    # Create a session from Python to the Database
    session = Session(engine)
    # Query for TMIN, TAVG, and TMAX for the given start date
    result = session.query(func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs)).filter(Measure.date >= start).all()
    # Convert the query results to a dictionary and return as JSON
    start_data = {"TMIN": result[0][0], "TAVG": result[0][1], "TMAX": result[0][2]}
    return jsonify(start_data)

# Define Start and end date temperature route
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    """Return a JSON list of the MIN, AVG and MAX temperatures for a given date range."""
    # Create a session from Python to the Database
    session = Session(engine)
    # Query for TMIN, TAVG, and TMAX between start and end dates
    result = session.query(func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs)).filter(Measure.date >= start).filter(Measure.date <= end).all()
    # Convert the query results to a dictionary and return as JSON
    start_end_data = {"TMIN": result[0][0], "TAVG": result[0][1], "TMAX": result[0][2]}
    return jsonify(start_end_data)

# Check if the file is being executed as the main program, and run the application in debug mode if it is
if __name__ == "__main__":
    app.run(debug=True)