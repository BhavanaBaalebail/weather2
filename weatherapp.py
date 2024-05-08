from flask import Flask, render_template, request
import requests
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    api_key = '403e4744a5ee5cab285bafbd8b9c366e'  # Replace with your actual API key
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']
        
        # Convert sunrise and sunset timestamps to readable format
        sunrise_time = datetime.utcfromtimestamp(sunrise).strftime('%Y-%m-%d %H:%M:%S')
        sunset_time = datetime.utcfromtimestamp(sunset).strftime('%Y-%m-%d %H:%M:%S')

        return render_template('weather.html', city=city, temperature=temperature, description=description,
                               humidity=humidity, wind_speed=wind_speed, sunrise=sunrise_time, sunset=sunset_time)
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return render_template('error.html')

if __name__ == '__main__':
    app.run(port=5031)