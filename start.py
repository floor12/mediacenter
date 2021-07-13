import yaml
from threading import Thread

from modules.Weather import Weather
from modules.WeatherProvider import *
from modules.VolumioStateProvider import *
from modules.VolumioState import *
from modules.Display import *
from modules.PowerController import *

with open(r'config.yaml') as file:
    config_list = yaml.load(file, Loader=yaml.FullLoader)

openWeatherToken = config_list['openWeatherApi']
openWeatherCityID = config_list['openWeatherCityID']
state = VolumioState()
weather = Weather()
oledDisplay = Display(state, weather)
volumioStateProvider = VolumioStateProvider(state)
powerController = PowerController(state)
WeatherProvider = WeatherProvider(weather, openWeatherToken, openWeatherCityID)


def display_thread():
    oledDisplay.render()


display_thread = Thread(target=display_thread)
display_thread.start()


def data_thread():
    volumioStateProvider.wait()


receive_thread = Thread(target=data_thread)
receive_thread.start()


def power_thread():
    powerController.check_playing_state()


power_thread = Thread(target=power_thread)
power_thread.start()


def weather_thread():
    WeatherProvider.checker()


weather_thread = Thread(target=weather_thread)
weather_thread.start()
