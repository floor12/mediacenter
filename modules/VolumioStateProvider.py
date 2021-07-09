

from socketIO_client import SocketIO
import json

class VolumioStateProvider():
  volumio_host = 'localhost'
  volumio_port = 3000
  volumioIO = SocketIO(volumio_host, volumio_port)
  
  isPlaying = False

  def __init__(self, state):
    self.state = state
    self.volumioIO.on('pushState', self.onPushState)
    self.volumioIO.emit('getState')


  def onPushState(self, data):
    print('new state received')
    print(data)
    self.state.currentState = data
 

  def wait(self):
    print('wailt')
    self.volumioIO.wait()
    while True:
      print('cycle1')
      sleep(1)

