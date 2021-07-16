import requests
import time


class WeatherProvider:
    API_URL = 'https://api.openweathermap.org/data/2.5/onecall'
    REFRESH_TIME = 60 * 5

    def __init__(self, weather, api_token, lon, lat):
        self.weather = weather
        self.api_token = api_token
        self.lon = lon
        self.lat = lat

    def start_loader(self):
        while True:
            self.load_weather()
            time.sleep(self.REFRESH_TIME)

    def load_weather(self):
        request_params = {
            'lon': self.lon,
            'lat': self.lat,
            'appid': self.api_token,
            'units': 'metric',
            'exclude': 'minutely,hourly,daily'
        }
        try:
            api_response = requests.get(url=self.API_URL, params=request_params)
            self.weather.set_new_data(api_response.json())
            print('weather updated')
            return True
        except:
            print('weather loading problem...')
            return False
