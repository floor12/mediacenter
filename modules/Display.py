from luma.core.interface.serial import spi
from luma.oled.device import ssd1322

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import time
from datetime import datetime as datetime


class Display():

  interface = spi(device=0, port=0)
  oled = ssd1322(interface, rotate=0) 
  width = 256
  height = 64
  fontBig = ImageFont.truetype("fonts/Comfortaa-VariableFont_wght.ttf", 64)
  fontMedium = ImageFont.truetype("fonts/Comfortaa-VariableFont_wght.ttf", 32)
  fontSmall = ImageFont.truetype("fonts/Comfortaa-VariableFont_wght.ttf", 25)
  scrollPosition = 0
  direction = 0
  lightColor = (200,200,200)
  darkColor = (100,100,100)
  currentColor = lightColor

  def __init__(self, state, weather):
    self.state = state
    self.weather = weather

  def render(self):    
   while True:
      image = Image.new('RGB', (self.width, self.width))
      draw = ImageDraw.Draw(image)		
      self.drawTemperature(draw)
      if (self.state.isPlaying() == True):
        self.playerScreen(draw)
        self.drawHumidity(draw,0)
      else:
        self.drawBigClock(draw)
        self.drawUV(draw)
        self.drawHumidity(draw,1)
      image.paste(image, (0, 0))
      cimg = image.crop((0, 0, self.width, self.height)) 
      self.oled.display(cimg)
      time.sleep(0.03)


  def drawBigClock(self, draw):
    draw.text((0,2), datetime.now().strftime("%H:%M"), font=self.fontBig, fill=self.currentColor)


  def drawTemperature(self, draw):
    if (self.weather.updatedAt > 0):
      temp = "+{:2.1f}".format(self.weather.getCurrentTemp())
      tempWidth, tempHeight = draw.textsize(temp, font=self.fontMedium)
      draw.text((self.width - tempWidth,0), temp, font=self.fontMedium, fill=self.currentColor)
    else:
      print('weather not loaded yet...')

  def drawHumidity(self, draw, row):
    if (self.weather.updatedAt > 0):
      temp = "{}%".format(self.weather.getCurrentHum())
      tempWidth, tempHeight = draw.textsize(temp, font=self.fontSmall)
      if row == 1:
        coord = (self.width - tempWidth,40)
        font = self.fontSmall
      else:
        font = self.fontMedium
        coord = (100, 0)
      draw.text(coord, temp, font=font, fill=self.currentColor)
    else:
      print('weather not loaded yet...')

  def drawUV(self, draw):
    if (self.weather.updatedAt > 0):
      uv = "{:0.0f}".format(self.weather.getCurrentUV())
      width, height = draw.textsize(uv, font=self.fontSmall)
      coord = (170, 40)
      draw.text(coord, uv, font=self.fontSmall, fill=self.currentColor)
    else:
      print('weather not loaded yet...')


  def playerScreen(self, draw):
    draw.text((0,0), datetime.now().strftime("%H:%M"), font=self.fontMedium, fill=self.currentColor)
    nowPlayng = self.state.currentState['artist'] + ': ' + self.state.currentState['title']

    ArtistWidth, ArtistHeight = draw.textsize(nowPlayng, font=self.fontMedium)
    if (ArtistWidth > self.width):

      if (self.direction == 0 and self.scrollPosition > ArtistWidth - self.width):
        self.direction = 1
        time.sleep(1)
      if (self.direction == 1 and self.scrollPosition == 0):
        self.direction = 0
        time.sleep(4)
      
      if (self.direction == 0):
        self.scrollPosition += 7
      else:
        self.scrollPosition -= 7

    else:
      self.scrollPosition = 0
      self.direction = 0

    draw.text((-self.scrollPosition,32), nowPlayng, font=self.fontMedium, fill=self.currentColor)




