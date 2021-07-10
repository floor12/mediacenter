import RPi.GPIO as GPIO
import time


class PowerController():
  lastTimePlayed = 0

  def __init__(self, state):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.OUT)
    self.state = state

  def checkPlaynigState(self): 
    while True:
      if ('service' in self.state.currentState):
        if (self.state.currentState['service'] == 'volspotconnect2'):
          GPIO.output(27, GPIO.HIGH)
        else:
          GPIO.output(27, GPIO.LOW)
      time.sleep(1)

