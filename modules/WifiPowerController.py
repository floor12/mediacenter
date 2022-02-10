import requests
import time


class WifiPowerController:
    PILOT_HOST = 'http://192.168.1.34/power'
    RELAY_AMPLIFY = 0
    RELAY_TURNTABLE = 1

    power_amplify = False
    power_turntable = False

    def __init__(self, state):
        self.state = state

    def start_listener(self):
        time.sleep(2)
        while True:
            self.check_volumio_state()
            self.check_power_state()
            time.sleep(3)

    def send_pilot_state(self,relay_num, mode):
        request_params = {
            'relay': relay_num,
            'power': mode,
        }
        try:
            api_response = requests.get(url=self.PILOT_HOST, params=request_params)
            response = api_response.text
            return True
        except:
            print('power state sending problem...')
            return False


    def check_power_state(self):
        if self.power_amplify:
            self.send_pilot_state(self.RELAY_AMPLIFY, 'on')
        else:
            self.send_pilot_state(self.RELAY_AMPLIFY, 'off')

        if self.power_turntable:
            self.send_pilot_state(self.RELAY_TURNTABLE, 'on')
        else:
            self.send_pilot_state(self.RELAY_TURNTABLE, 'off')

    def check_volumio_state(self):
        if self.state.get_playing_mode() == self.state.MODE_TURNTABLE:
            self.power_amplify = True
            self.power_turntable = True
        else:
            if self.state.get_playing_mode() == self.state.MODE_DIGITAL:
                self.power_amplify = True
                self.power_turntable = False
            else:
                self.power_amplify = False
                self.power_turntable = False
