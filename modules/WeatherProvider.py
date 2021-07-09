import requests
import time
from modules.Weather import *

class WeatherProvider():
  cityId = 2509954
  apiToken = 'd7807f91fdd6c905fee984793c793f10'
  apiUrl = 'https://adddpi.openweathermap.org/data/2.5/onecall'
  refreshTime = 60 * 15 

  def __init__(self, weather):
    self.weather = weather

  def checker(self):
    while True:
      self.loadWeather()
      time.sleep(self.refreshTime)


  def loadWeather(self):
    requestParams = {
    #  'id': self.cityId, 
      'lon': -0.3774, 
      'lat': 39.4697,
      'appid': self.apiToken, 
      'units': 'metric',
      'exclude': 'minutely,houly,daily'
    }
    apiResponse = requests.get(url = self.apiUrl, params = requestParams)
    self.weather.currentWeather = apiResponse.json()
    self.weather.updatedAt = time.time()
    print('weather updated')
    print(self.weather.currentWeather)

  
  
  