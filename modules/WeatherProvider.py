import requests
import time
from modules.Weather import *

class WeatherProvider():
  apiUrl = 'https://api.openweathermap.org/data/2.5/onecall'
  refreshTime = 60 * 5

  def __init__(self, weather,apiToken, cityId):
    self.weather = weather
    self.apiToken = apiToken
    self.cityId = cityId

  def checker(self):
    while True:
      self.loadWeather()
      time.sleep(self.refreshTime)


  def loadWeather(self):
    requestParams = {
      'lon': -0.3774, 
      'lat': 39.4697,
      'appid': self.apiToken, 
      'units': 'metric',
      'exclude': 'minutely,houly,daily'
    }
    try:
      apiResponse = requests.get(url = self.apiUrl, params = requestParams)
      self.weather.currentWeather = apiResponse.json()
      self.weather.updatedAt = time.time()
      print('weather updated')
    except requests.exceptions.RequestException as e:
      print('weather loading problem...')


  
  
  