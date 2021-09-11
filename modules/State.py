import time


class State:
    IDLE_PERIOD = 60
    MODE_IDLE = 0
    MODE_DIGITAL = 1
    MODE_TURNTABLE = 2

    is_digital_active = False
    is_turntable_active = False
    last_digital_active = 0
    volumio_state = {'status': 'stop'}

    def set_state(self, state):
        self.volumio_state = state
        self.last_digital_active = time.time()
        print(self.volumio_state)
        if self.volumio_state['status'] == 'play':
            self.is_digital_active = True
        else:
            self.is_digital_active = False

    def get_playing_mode(self):
        if self.is_turntable_active:
            return self.MODE_TURNTABLE
        if self.is_digital_active:
            return self.MODE_DIGITAL
        if self.last_digital_active + self.IDLE_PERIOD >= time.time() and 'service' in self.volumio_state and \
                (self.volumio_state['service'] == 'volspotconnect2' or self.volumio_state['service'] == 'airplay_emulation'):
            return self.MODE_DIGITAL
        return self.MODE_IDLE
