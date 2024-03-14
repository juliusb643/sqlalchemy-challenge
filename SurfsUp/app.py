import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
        return (
            f"Available Routes: <br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end><br/>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    data_query = session.query(Measurement.prcp, Measurement.date)\
    .filter(Measurement.date > '2016-08-23')\
    .filter(Measurement.date < '2017-08-23')\
    .group_by(Measurement.date)\
    .order_by(Measurement.date)\
    .all()
    session.close()

    precipitation_data = {}

    for data in data_query:
        date = result["date"]
        prcp = result["prcp"]
        precipitation_data[date] = prcp

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station).all()
    session.close()

    station_names = list(np.ravel(stations))

    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    latest_date = session.query(func.max(Measurement.date)).scalar()
    start_date = dt.datetime.strptime(latest_date, '%Y-%m-%d') - dt.timedelta(days=365)

    tobs_data = session.query(Measurement.tobs)\
    .filter(Measurement.station == 'USC00519281')\
    .filter(Measurement.date >= start_date)\
    .all()
    session.close()

    return jsonify(tobs_data)

@app.route("/api/v1.0/start/<start>")
def start():
    session = Session(engine)
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)) \
    .first()

    lowest_temp, highest_temp, avg_temp = result

    print(f"Lowest Temperature: {lowest_temp}")
    print(f"Highest Temperature: {highest_temp}")
    print(f"Average Temperature: {avg_temp}")

    return jsonify({
        'start_date': start_date,
        'min_temperature': lowest_temp,
        'max_temperature': highest_temp,
        'avg_temperature': avg_temp
    })

@app.route("/api/v1.0/start/end/<start>/<end>")
def start_end():
    session = Session(engine)
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)) \
    .first()

    filtered_data = {date: tobs for date in result if start_date <= datetime.strptime(date, '%Y-%m-%d') <= end_date}

    if not filtered_data:
        return jsonify({'message': 'No temperature data available for the specified date range'})

    min_temp = min(filtered_data.values())
    max_temp = max(filtered_data.values())
    avg_temp = sum(filtered_data.values()) / len(filtered_data)

    return jsonify({
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'min_temperature': min_temp,
        'max_temperature': max_temp,
        'avg_temperature': avg_temp
    })

if __name__ == '__main__':
    app.run(debug=True)
    
    

