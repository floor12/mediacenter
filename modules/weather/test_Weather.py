from Weather import *

test_json = {'lat': 39.4697, 'lon': -0.3774, 'timezone': 'Europe/Madrid', 'timezone_offset': 7200,
             'current': {'dt': 1626434619, 'sunrise': 1626410847, 'sunset': 1626463637, 'temp': 28.00,
                         'feels_like': 29.29, 'pressure': 1017, 'humidity': 58, 'dew_point': 19.01, 'uvi': 8.45,
                         'clouds': 0, 'visibility': 10000, 'wind_speed': 0.45, 'wind_deg': 271, 'wind_gust': 0.89,
                         'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}]}}


def test_no_current_weather():
    weather = Weather()
    assert weather.get_current_temp() == 0
    assert weather.get_current_uv() == 0
    assert weather.get_current_uv() == 0
    assert weather.has_data() == False


def test_set_data():
    weather = Weather()
    weather.set_new_data(test_json)
    assert weather.has_data() == True

def test_get_temp():
    weather = Weather()
    weather.set_new_data(test_json)
    assert weather.get_current_temp() == 28.00

def test_get_hum():
    weather = Weather()
    weather.set_new_data(test_json)
    assert weather.get_current_hum() == 58

def test_get_uv():
    weather = Weather()
    weather.set_new_data(test_json)
    assert weather.get_current_uv() == 84.5
