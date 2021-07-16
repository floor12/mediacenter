from luma.core.interface.serial import spi
from luma.oled.device import ssd1322

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import time
from datetime import datetime as datetime


class Display:
    interface = spi(device=0, port=0)
    oled = ssd1322(interface, rotate=0)
    width = 256
    height = 64
    fontBig = ImageFont.truetype("fonts/Comfortaa-VariableFont_wght.ttf", 64)
    font_medium = ImageFont.truetype("fonts/Comfortaa-VariableFont_wght.ttf", 32)
    fontSmall = ImageFont.truetype("fonts/Comfortaa-VariableFont_wght.ttf", 25)
    scrollPosition = 0
    direction = 0
    lightColor = (200, 200, 200)
    darkColor = (100, 100, 100)
    current_color = darkColor

    def __init__(self, state, weather):
        self.state = state
        self.weather = weather

    def render(self):
        while True:
            image = Image.new('RGB', (self.width, self.width))
            draw = ImageDraw.Draw(image)
            self.draw_temperature(draw)

            if self.state.get_playing_mode() == self.state.MODE_DIGITAL:
                self.draw_current_track(draw)
                self.draw_small_clock(draw)
                self.draw_humidity(draw, 0)
            else:
                if self.state.get_playing_mode() == self.state.MODE_TURNTABLE:
                    self.draw_turntable(draw)
                    self.draw_small_clock(draw)
                    self.draw_humidity(draw, 0)
                else:
                    self.draw_big_clock(draw)
                    self.draw_uv(draw)
                    self.draw_humidity(draw, 1)
            image.paste(image, (0, 0))
            cimg = image.crop((0, 0, self.width, self.height))
            self.oled.display(cimg)
            time.sleep(0.03)

    def draw_big_clock(self, draw):
        draw.text((0, 2), datetime.now().strftime("%H:%M"), font=self.fontBig, fill=self.current_color)

    def draw_temperature(self, draw):
        if self.weather.updated_at > 0:
            temp = "+{:2.1f}".format(self.weather.get_current_temp())
            temp_width, temp_height = draw.textsize(temp, font=self.font_medium)
            draw.text((self.width - temp_width, 0), temp, font=self.font_medium, fill=self.current_color)
        else:
            print('weather not loaded yet...')

    def draw_humidity(self, draw, row):
        if self.weather.updated_at > 0:
            temp = "{}%".format(self.weather.get_current_hum())
            temp_width, temp_height = draw.textsize(temp, font=self.fontSmall)
            if row == 1:
                coord = (self.width - temp_width, 40)
                font = self.fontSmall
            else:
                font = self.font_medium
                coord = (100, 0)
            draw.text(coord, temp, font=font, fill=self.current_color)
        else:
            print('weather not loaded yet...')

    def draw_uv(self, draw):
        if self.weather.updated_at > 0:
            uv = "{:0.0f}".format(self.weather.get_current_uv())
            coord = (170, 40)
            draw.text(coord, uv, font=self.fontSmall, fill=self.current_color)
        else:
            print('weather not loaded yet...')

    def draw_current_track(self, draw):
        now_playing = self.state.volumio_state['artist'] + ': ' + self.state.volumio_state['title']

        artist_width, artist_height = draw.textsize(now_playing, font=self.font_medium)
        if artist_width > self.width:

            if self.direction == 0 and self.scrollPosition > artist_width - self.width:
                self.direction = 1
                time.sleep(1)
            if self.direction == 1 and self.scrollPosition == 0:
                self.direction = 0
                time.sleep(4)

            if self.direction == 0:
                self.scrollPosition += 7
            else:
                self.scrollPosition -= 7

        else:
            self.scrollPosition = 0
            self.direction = 0

        draw.text((-self.scrollPosition, 32), now_playing, font=self.font_medium, fill=self.current_color)

    def draw_small_clock(self, draw):
        draw.text((0, 0), datetime.now().strftime("%H:%M"), font=self.font_medium, fill=self.current_color)

    def draw_turntable(self, draw):
        draw.text((30, 32), 'Вертушка', font=self.font_medium, fill=self.current_color)
