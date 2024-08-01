# app.py
from flask import Flask, render_template, request
import requests
from config import API_KEY

app = Flask(__name__)


def get_weather(city_name):
    """
    Function to get the weather data from OpenWeatherMap API.
    """
    # Construct the API URL with the city name and API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"

    # Make a request to the OpenWeatherMap API
    response = requests.get(url)

    # If the response was successful, no Exception will be raised
    response.raise_for_status()

    # Return the JSON response
    return response.json()


@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        city_name = request.form.get('city')

        try:
            weather_data = get_weather(city_name)
        except requests.HTTPError as http_err:
            error = f"HTTP error occurred: {http_err}"
        except Exception as err:
            error = f"Other error occurred: {err}"

    return render_template('index.html', weather_data=weather_data, error=error)


if __name__ == '__main__':
    app.run(debug=True)
