from lib.Ultradrive import *


class UltradriveController:
    ultradrive = None

    def __init__(self, state):
        self.state = state
        self.connect()

    def control_device(self):
        while True:
            time.sleep(3)
            self.ultradrive.enable_listen()
            if self.state.get_playing_mode() == self.state.MODE_TURNTABLE:
                self.send_turntable_commands()
            if self.state.get_playing_mode() == self.state.MODE_DIGITAL:
                self.send_digital_commands()

    def send_turntable_commands(self):
        print('switch ultradrive to analog')
        # switch to analog
        self.ultradrive.set_value(
            self.ultradrive.channels['channelSetup'],
            self.ultradrive.commands['setup']['ono_ff'],
            0
        )

        # set input volume
        self.ultradrive.set_value(
            self.ultradrive.channels['inputB'],
            self.ultradrive.commands['in_out']['gain'],
            self.ultradrive.convert_db(-3)
        )

        self.ultradrive.set_value(
            self.ultradrive.channels['inputC'],
            self.ultradrive.commands['in_out']['gain'],
            self.ultradrive.convert_db(-3)
        )

        # switch inputs
        self.ultradrive.set_value(
            self.ultradrive.channels['output1'],
            self.ultradrive.commands['out']['input_source'],
            1
        )
        self.ultradrive.set_value(
            self.ultradrive.channels['output2'],
            self.ultradrive.commands['out']['input_source'],
            1
        )
        self.ultradrive.set_value(
            self.ultradrive.channels['output3'],
            self.ultradrive.commands['out']['input_source'],
            1
        )
        self.ultradrive.set_value(
            self.ultradrive.channels['output4'],
            self.ultradrive.commands['out']['input_source'],
            2
        )
        self.ultradrive.set_value(
            self.ultradrive.channels['output5'],
            self.ultradrive.commands['out']['input_source'],
            2
        )
        self.ultradrive.set_value(
            self.ultradrive.channels['output6'],
            self.ultradrive.commands['out']['input_source'],
            2
        )

    def send_digital_commands(self):
        print('switch ultradrive to digital')
        # switch to analog
        self.ultradrive.set_value(
            self.ultradrive.channels['channelSetup'],
            self.ultradrive.commands['setup']['ono_ff'],
            1
        )

        # set input volume
        self.ultradrive.set_value(
            self.ultradrive.channels['inputB'],
            self.ultradrive.commands['in_out']['gain'],
            self.ultradrive.convert_db(-7)
        )

        self.ultradrive.set_value(
            self.ultradrive.channels['inputC'],
            self.ultradrive.commands['in_out']['gain'],
            self.ultradrive.convert_db(-7)
        )

        # switch inputs
        self.ultradrive.set_value(
            self.ultradrive.channels['output1'],
            self.ultradrive.commands['out']['input_source'],
            0
        )
        self.ultradrive.set_value(
            self.ultradrive.channels['output2'],
            self.ultradrive.commands['out']['input_source'],
            0
        )
        self.ultradrive.set_value(
            self.ultradrive.channels['output3'],
            self.ultradrive.commands['out']['input_source'],
            0
        )
        self.ultradrive.set_value(
            self.ultradrive.channels['output4'],
            self.ultradrive.commands['out']['input_source'],
            1
        )
        self.ultradrive.set_value(
            self.ultradrive.channels['output5'],
            self.ultradrive.commands['out']['input_source'],
            1
        )
        self.ultradrive.set_value(
            self.ultradrive.channels['output6'],
            self.ultradrive.commands['out']['input_source'],
            1
        )

    def connect(self):
        if self.ultradrive is None:
            try:
                self.ultradrive = Ultradrive('/dev/ttyUSB0')
                print('Connected to Ultradrive')
            except EOFError:
                print('Could not connect to Ultradrive')
