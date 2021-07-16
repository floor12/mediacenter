import time

from socketIO_client import SocketIO


class VolumioStateProvider:
    volumio_host = 'localhost'
    volumio_port = 3000
    volumioIO = SocketIO(volumio_host, volumio_port)

    is_playing = False

    def __init__(self, state):
        self.state = state
        self.volumioIO.on('pushState', self.on_push_state)
        self.volumioIO.emit('getState')

    def on_push_state(self, data):
        print('new state received')
        self.state.set_state(data)

    def start_listener(self):
        print('wait')
        self.volumioIO.wait()
        while True:
            print('cycle1')
            time.sleep(1)
