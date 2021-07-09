
class Weather():
  currentWeather = {}
  updatedAt = 0


  def getCurrentTemp(self):
    return self.currentWeather['current']['temp']

  def getCurrentHum(self):
    return self.currentWeather['current']['humidity']

  def getCurrentUV(self):
    return self.currentWeather['current']['uvi']*10