class VolumioState:
    current_state = {'status': 'stop'}

    def is_playing(self):
        if self.current_state['status'] == 'play':
            return True
        else:
            return False
