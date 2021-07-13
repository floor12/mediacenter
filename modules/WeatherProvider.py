import requests
import time


class WeatherProvider:
    apiUrl = 'https://api.openweathermap.org/data/2.5/onecall'
    refreshTime = 60 * 5

    def __init__(self, weather, api_token, city_id):
        self.weather = weather
        self.api_token = api_token
        self.city_id = city_id

    def checker(self):
        while True:
            self.load_weather()
            time.sleep(self.refreshTime)

    def load_weather(self):
        request_params = {
            'lon': -0.3774,
            'lat': 39.4697,
            'appid': self.api_token,
            'units': 'metric',
            'exclude': 'minutely,hourly,daily'
        }
        try:
            api_response = requests.get(url=self.apiUrl, params=request_params)
            self.weather.current_weather = api_response.json()
            self.weather.updated_at = time.time()
            print('weather updated')
        except requests.exceptions.RequestException:
            print('weather loading problem...')
