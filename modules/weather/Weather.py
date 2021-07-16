import time


class Weather:
    __open_weather_data = {}
    __updated_at = 0

    def set_new_data(self, data):
        self.__open_weather_data = data
        self.__updated_at = time.time()

    def get_current_temp(self) -> object:
        if not self.has_data():
            return 0
        return self.__open_weather_data['current']['temp']

    def get_current_hum(self):
        if not self.has_data():
            return 0
        return self.__open_weather_data['current']['humidity']

    def get_current_uv(self):
        if not self.has_data():
            return 0
        return self.__open_weather_data['current']['uvi'] * 10

    def has_data(self):
        return self.__updated_at > 0
