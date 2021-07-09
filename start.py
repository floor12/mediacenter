
import time
from threading import Thread
from modules.Weather import *
from modules.WeatherProvider import *
from modules.VolumioStateProvider import *
from modules.VolumioState import *
from modules.Display import *
from modules.PowerController import *


state = VolumioState();
weather = Weather();
oledDisplay = Display(state, weather);
volumioStateProvider = VolumioStateProvider(state)
powerController = PowerController(state)
WeatherProvider = WeatherProvider(weather)

def displayThread():
	oledDisplay.render()
display_thread = Thread(target=displayThread)
display_thread.start()


def dataThread():
	volumioStateProvider.wait()
receive_thread = Thread(target=dataThread)
receive_thread.start()


def powerThread():
	powerController.checkPlaynigState()
power_thread = Thread(target=powerThread)
power_thread.start()

def weatherThread():
  WeatherProvider.checker()
weather_thread = Thread(target=weatherThread)
weather_thread.start()
