import RPi.GPIO as GPIO
import time


class PowerController:
    PIN_AMPLIFY = 27
    PIN_TURNTABLE = 17

    power_amplify = False
    power_turntable = False

    def __init__(self, state):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN_AMPLIFY, GPIO.OUT)
        GPIO.setup(self.PIN_TURNTABLE, GPIO.OUT)
        self.state = state

    def check_playing_state(self):
        time.sleep(2)
        while True:
            self.check_volumio_state()
            self.check_power_state()
            time.sleep(1)

    def check_power_state(self):
        if self.power_amplify:
            GPIO.output(self.PIN_AMPLIFY, GPIO.HIGH)
        else:
            GPIO.output(self.PIN_AMPLIFY, GPIO.LOW)

        if self.power_turntable:
            GPIO.output(self.PIN_TURNTABLE, GPIO.HIGH)
        else:
            GPIO.output(self.PIN_TURNTABLE, GPIO.LOW)

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
