import keyboard


class KeyboardProvider:
    TURNTABLE_CODE = 6
    PLAY_PAUSE_CODE = 2

    def __init__(self, stateProvider):
        self.stateProvider = stateProvider
        keyboard.on_release(self.key_release)

    def key_release(self, event):
        if self.TURNTABLE_CODE == event.scan_code:
            print('turntable button pressed')
            self.stateProvider.state.is_turntable_active = not self.stateProvider.state.is_turntable_active

        if self.PLAY_PAUSE_CODE == event.scan_code:
            print('play/pause button pressed')
            self.stateProvider.toggle_play()

        if event.scan_code == 3:
            self.stateProvider.stop()

        if event.scan_code == 4:
            self.stateProvider.prev()

        if event.scan_code == 5:
            self.stateProvider.next()
