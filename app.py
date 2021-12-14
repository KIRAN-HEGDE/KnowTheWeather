from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from api.WeatherData import WeatherData
from . import db
from .model import User

import requests
import json

app = Blueprint('app', __name__)

@app.route('/')
@login_required
def index():
    return render_template('index.html', name=current_user.firstName)

@app.route('/details')
@login_required
def details():
    user = User.query.get_or_404(current_user.id)
    latitude = str(user.latitude)
    longitude = str(user.longitude)

    api_id = '1c2e706a6a347e137b47207ca013c8da'
    response_API = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat='+latitude+'&lon='+longitude+'&appid='+api_id)
    
    if response_API.status_code == 200:  
        data = response_API.text
        parse_json = json.loads(data)
        return render_template('weatherDetails.html', 
                                latitude=parse_json['lat'], 
                                longitude=parse_json['lon'], 
                                timezone=parse_json['timezone'], 
                                temp=parse_json['current']['temp'],   
                                pressure=parse_json['current']['pressure'],
                                main=parse_json['current']['weather'][0]['main'],
                                description=parse_json['current']['weather'][0]['description'],  
                                name=current_user.firstName
                            )

    return render_template('index.html', name=current_user.firstName)

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
        return render_template('index.html', name=current_user.firstName)


    return render_template('weatherDetails.html',
                                latitude=data.co_ordinates['lat'],
                                longitude=data.co_ordinates['lon'],
                                timezone=daily_data.time_zone,
                                temp=data.temp_details['temp'],
                                pressure=data.temp_details['pressure'],
                                main=data.weather_desc['main'],
                                description=data.weather_desc['description'],
                                name=current_user.firstName
                            )

