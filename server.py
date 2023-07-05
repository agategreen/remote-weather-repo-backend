from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import json


app = Flask(__name__)
CORS(app)

@app.route('/weather')
@cross_origin() 
def get_weather():

    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    api_key = 'fb7e3d6e6417bae7fadf83a42f83c674'

    try:
        url_current = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'
        response = requests.get(url_current)
        data = response.json()
        data_current = data

        url_forecast = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric'
        response = requests.get(url_forecast)
        data = response.json()

        forecast_list = data["list"]
        date_set = set()
        for forecast in forecast_list:
            dt_txt = forecast["dt_txt"]
            date = dt_txt[:10]
            date_set.add(date)

        minTemp_dict = {}
        maxTemp_dict = {}
        for element in date_set:
            minTemp_dict[element] = []
            maxTemp_dict[element] = []

        for forecast in forecast_list:
            dt_txt = forecast["dt_txt"]
            date = dt_txt[:10]

            minTemp_dict[date].append(forecast["main"]["temp_min"]) 
            maxTemp_dict[date].append(forecast["main"]["temp_max"]) 
        
        final_data = {
            "current":{
                "weather_condition":data_current["weather"][0]["main"],
                "temp": data_current["main"]["temp"],
                "humidity":data_current["main"]["humidity"],
                "speed":data_current["wind"]["speed"]

            },
            "forecast":[]
        }

        for element in date_set:
            forecast_data = {
                "dt_txt": element,
                "temp_min":min(minTemp_dict[element]),
                "temp_max":max(maxTemp_dict[element])
                }
            final_data["forecast"].append(forecast_data)

        
        return jsonify(final_data)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run()
