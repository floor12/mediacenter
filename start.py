import yaml
from threading import Thread

from modules.weather.Weather import *
from modules.weather.WeatherProvider import *
from modules.KeyboardProvider import *
from modules.VolumioStateProvider import *
from modules.State import *
from modules.Display import *
from modules.PowerController import *
from modules.UltradriveController import *

with open(r'config.yaml') as file:
    config_list = yaml.load(file, Loader=yaml.FullLoader)

openWeatherToken = config_list['openWeatherApi']
openWeatherLon = config_list['openWeatherLon']
openWeatherLat = config_list['openWeatherLat']
state = State()
weather = Weather()
oledDisplay = Display(state, weather)
volumioStateProvider = VolumioStateProvider(state)
powerController = PowerController(state)
ultradriveController = UltradriveController(state)
WeatherProvider = WeatherProvider(weather, openWeatherToken, openWeatherLon, openWeatherLat)
KeyboardProvider = KeyboardProvider(volumioStateProvider)


def display_thread():
    oledDisplay.render()


display_thread = Thread(target=display_thread)
display_thread.start()


def data_thread():
    volumioStateProvider.start_listener()


receive_thread = Thread(target=data_thread)
receive_thread.start()


def power_thread():
    powerController.start_listener()


power_thread = Thread(target=power_thread)
power_thread.start()


def weather_thread():
    WeatherProvider.start_loader()


weather_thread = Thread(target=weather_thread)
weather_thread.start()


def ultradrive_thread():
    ultradriveController.control_device()


ultradrive_thread = Thread(target=ultradrive_thread)
ultradrive_thread.start()

# !!! GPIO buttons thread is disabled  !!!
#
# def buttons_thread():
#     ButtonProvider.start_listener()
#
#
# buttons_thread = Thread(target=buttons_thread)
# buttons_thread.start()
