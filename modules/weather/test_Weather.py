from Weather import *

test_json = {'current': {'temp': 28.00, 'humidity': 58, 'uvi': 8.45}}


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
