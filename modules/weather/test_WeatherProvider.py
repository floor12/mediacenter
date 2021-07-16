from WeatherProvider import *
from Weather import *

test_json = '{"current": {"temp": 28.00, "humidity": 58, "uvi": 8.45}}'
api_token = 'some_test_key'
lon = 30
lat = -30

def test_load_weather_fail(requests_mock):
    weather = Weather()
    provider = WeatherProvider(weather, api_token, lon, lat)
    requests_mock.get(provider.API_URL)
    assert provider.load_weather() == False
    assert weather.has_data() == False


def test_load_weather_success(requests_mock):
    weather = Weather()
    provider = WeatherProvider(weather, api_token, lon, lat)
    requests_mock.get(provider.API_URL, text=test_json)
    assert provider.load_weather() == True
    assert weather.has_data() == True
