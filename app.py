#import dependencies
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#database setup
engine = create_engine('sqlite:///hawaii.sqlite')

#create base
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#flask setup
app = Flask(__name__)

#flask routes
@app.route('/')
def welcome():
    '''List all available api routes.'''
    return (
        f'Welcome to Hawaii!<br/>'
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start'
        f'/api/v1.0/<start>/<end>'
    )

#create precipitation route
@app.route('/api/v1.0/precipitation')
def precipitation():

    session = Session(engine)

    results=session.query(Measurement.date,Measurement.prcp).all()
    session.close()

    precipitation = []
    for date,prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        precipitation.append(prcp_dict)
        
    return jsonify(precipitation)

#create a station route
@app.route('/api/v1.0/stations')
def stations():
    
    session = Session(engine)
    results = session.query(Station.name,Station.station).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

#create tobs route
@app.route('/api/v1.0/tobs')
def tobs():

    session = Session(engine)
    recent_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= recent_year).all()
    session.close()

    tobs_data = list(np.ravel(tobs))
    return jsonify(tobs_data)


#create start route
@app.route('/api/v1.0/start') 
def start():

    session = Session(engine)

    start_date = session.query(func.min(Measurement.date))
   
    results = session.query(func.min(Measurement.tobs),
     func.avg(Measurement.tobs),
      func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close

    start = list(np.ravel(results))
    return jsonify(start)    






if __name__ == "__main__":
    app.run(debug=True)