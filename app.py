from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from .api.WeatherData import WeatherData
from . import db
from .model import User

import requests
import json

app = Blueprint('app', __name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/locate')
@login_required
def locate():
    return render_template('selectLocation.html')

@app.route('/details')
@login_required
def details():
    user = User.query.get_or_404(current_user.id)
    latitude = str(user.latitude)
    longitude = str(user.longitude)


    try:
        weather_data = WeatherData.by_latitude_longitude(latitude, longitude)
        data = weather_data.current_data
        daily_data = weather_data.daily_data
    except Exception:
        print("API unreachable")
        return render_template('index.html')


    return render_template('weatherDetails.html',
                                latitude=data.co_ordinates['lat'],
                                longitude=data.co_ordinates['lon'],
                                timezone=daily_data.time_zone,
                                temp=data.temp_details['temp'],
                                pressure=data.temp_details['pressure'],
                                main=data.weather_desc['main'],
                                description=data.weather_desc['description']
                            )

@app.route('/details', methods=['POST'])
@login_required
def weatherDetails_post():
    
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    user = User.query.get_or_404(current_user.id)
    if latitude == None and longitude == None:
        latitude = str(user.latitude)
        longitude = str(user.longitude)

    user.latitude = float(latitude)
    user.longitude = float(longitude)
    db.session.commit()


    try:
        weather_data = WeatherData.by_latitude_longitude(latitude, longitude)
        data = weather_data.current_data
        daily_data = weather_data.daily_data
    except Exception:
        print("API unreachable")
        return render_template('index.html')


    return render_template('weatherDetails.html',
                                latitude=data.co_ordinates['lat'],
                                longitude=data.co_ordinates['lon'],
                                timezone=daily_data.time_zone,
                                temp=data.temp_details['temp'],
                                pressure=data.temp_details['pressure'],
                                main=data.weather_desc['main'],
                                description=data.weather_desc['description']
                            )