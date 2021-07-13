import RPi.GPIO as GPIO
import time


class PowerController:
    last_time_played = 0

    def __init__(self, state):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(27, GPIO.OUT)
        self.state = state

    def check_playing_state(self):
        while True:
            if 'service' in self.state.current_state:
                if self.state.current_state['service'] == 'volspotconnect2':
                    GPIO.output(27, GPIO.HIGH)
                else:
                    GPIO.output(27, GPIO.LOW)
            time.sleep(1)
