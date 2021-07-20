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
        self.volumioIO.wait()
        while True:
            time.sleep(1)

    def toggle_play(self):
        if 'status' in self.state.volumio_state and self.state.volumio_state['status'] == 'play':
            self.volumioIO.emit('pause')
            print('pause emited')
            time.sleep(1)
            self.volumioIO.emit('getState')
        else:
            self.volumioIO.emit('play')
            print('play emited')
            time.sleep(1)
            self.volumioIO.emit('getState')

    def next(self):
        self.volumioIO.emit('next')
        print('next emited')

    def prev(self):
        self.volumioIO.emit('prev')
        print('prev emited')

    def stop(self):
        self.volumioIO.emit('stop')
        print('stop emited')
        time.sleep(1)
        self.volumioIO.emit('getState')

