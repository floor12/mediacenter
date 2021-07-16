import time

import RPi.GPIO as GPIO


class ButtonProvider:
    PIN_TURNTABLE_POWER = 4

    is_playing = False

    def __init__(self, state):
        self.state = state
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN_TURNTABLE_POWER, GPIO.IN)

    def start_listener(self):
        while True:
            self.read_turntable_button()
            time.sleep(1)

    def read_turntable_button(self):
        pin_value = GPIO.input(self.PIN_TURNTABLE_POWER)
        if pin_value == 1:
            self.state.is_turntable_active = True
        else:
            self.state.is_turntable_active = False
