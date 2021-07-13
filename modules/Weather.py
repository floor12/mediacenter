class Weather:
    current_weather = {}
    updated_at = 0

    def get_current_temp(self):
        return self.current_weather['current']['temp']

    def get_current_hum(self):
        return self.current_weather['current']['humidity']

    def get_current_uv(self):
        return self.current_weather['current']['uvi'] * 10
