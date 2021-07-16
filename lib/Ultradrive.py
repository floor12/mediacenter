import time

import serial


class Ultradrive:
    channels = {
        "channelSetup": 0x00,
        "inputA": 0x01,
        "inputB": 0x02,
        "inputC": 0x03,
        "inputSUM": 0x04,
        "output1": 0x05,
        "output2": 0x06,
        "output3": 0x07,
        "output4": 0x08,
        "output5": 0x09,
        "output6": 0x0A,
    }

    commands = {
        'setup': {
            "input_sum_type": 0x02,  # off, A, B, C, A+B, A+C, B+C
            "ono_ff": 0x03,
            "input_c_gain": 0x04,
            "output_config": 0x05,  # MONO, LMHLMH, LLMMHH, LHLHLH
            "stereo_link": 0x06,
            "in_stereo_link": 0x07,  # off, a+b, a+b+c, a+b+c+sum
            "delay_link": 0x08,
            "xover_link": 0x09,
            "delay_correction": 0x0A,
            "air_temp": 0x0B,  # 0..70 (-20..+50 (deg centigrade always))
            "delay_units": 0x14,  # 0:mm, 1:inch
            "mute_outs": 0x15,
            "in_a_sum_gain": 0x16,
            "in_b_sum_gain": 0x17,
            "in_c_sum_gain": 0x18,
        },
        'in_out': {
            "gain": 0x02,
            "mute": 0x03,
            "delay_on": 0x04,
            "delay_value": 0x05,
            "eq_on": 0x06,
            "eq_number": 0x07,
            "eq_index": 0x08,
            "dyn_eq_attack_index": 0x09,
            "dyn_eq_release": 0x0A,
            "dyn_eq_ration": 0x0B,
            "dyn_eq_thresh": 0x0C,
            "dyn_eq_switch": 0x0D,
            "dyn_eq_freq": 0x0E,  # (20..20k log)
            "dyn eq_q": 0x0F,  # (0.1..10 log)
            "dyn_eq_gain": 0x10,  # (-15..+15dB, step 0.1dB)
            "dyn_eq filter ": 0x11,  # (0:low shelv, 1:bandpass, 2:hi shelv)
            "dyn_eq_shelv_slope": 0x12,  # (0:6dB, 1:12dB)
            'eq_1_freq': 0x13,
            'eq_1_q': 0x14,
            'eq_1_gain': 0x15,
            'eq_1_filter': 0x16,
            'eq_1_shelv slope': 0x17,
            'eq_2_freq': 0x18,
            'eq_2_q': 0x19,
            'eq_2_gain': 0x1A,
            'eq_2_filter': 0x1B,
            'eq_2_shelv slope': 0x1C,
            'eq_3_freq': 0x1D,
            'eq_3_q': 0x1E,
            'eq_3_gain': 0x1F,
            'eq_3_filter': 0x20,
            'eq_3_shelv slope': 0x21,
            'eq_4_freq': 0x22,
            'eq_4_q': 0x23,
            'eq_4_gain': 0x24,
            'eq_4_filter': 0x25,
            'eq_4_shelv slope': 0x26,
            'eq_5_freq': 0x27,
            'eq_5_q': 0x28,
            'eq_5_gain': 0x29,
            'eq_5_filter': 0x2A,
            'eq_5_shelv slope': 0x2B,
            'eq_6_freq': 0x2C,
            'eq_6_q': 0x2D,
            'eq_6_gain': 0x2E,
            'eq_6_filter': 0x2F,
            'eq_6_shelv slope': 0x30,
            'eq_7_freq': 0x31,
            'eq_7_q': 0x32,
            'eq_7_gain': 0x33,
            'eq_7_filter': 0x34,
            'eq_7_shelv slope': 0x35,
            'eq_8_freq': 0x36,
            'eq_8_q': 0x37,
            'eq_8_gain': 0x38,
            'eq_8_filter': 0x39,
            'eq_8_shelv slope': 0x3A,
            'eq_9_freq': 0x3B,
            'eq_9_q': 0x3C,
            'eq_9_gain': 0x3D,
            'eq_9_filter': 0x3E,
            'eq_0_shelv slope': 0x3F,
        },
        'out': {
            "name": 0x40,
            "input_source": 0x41,  # 0..3 (A, B, C, SUM)
            "hp_filter": 0x42,  # 0..10 (off, but6, but12, bes12, lr12, but18, but, bes24, lr24, but48, lr48)
            "hp_freq": 0x43,  # 0..320 (20..20k log)
            "lp_filter": 0x44,  # 0..10 (off, but6, but12, bes12, lr12, but18, but, bes24, lr24, but48, lr48)
            "lp_freq": 0x45,  # 0..320 (20..20k log)
            "limiter_on": 0x46,  # (1:on)
            "limiter_thresh": 0x47,  # 0..240 (-24..0dB step 0.1dB)
            "limiter_release": 0x48,  # 0..251 (20..4000ms log)
            "polarity": 0x49,  # (1:inverse)
            "phase": 0x4A,  # 0..36 (0..180deg step 5deg)
            "short delay": 0x4B,  # 0..2000 (0..4000mm step 2mm)
        }
    }

    def __init__(self, serial_path):
        self.ser = serial.Serial(
            port=serial_path,
            baudrate=38400,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        self.enable_listen()

    def set_value(self, channel, param, value):
        self.send_command(self.prepare_command(channel, param, value))

    @staticmethod
    def prepare_command(channel, param, value):
        value_hi = value // 128
        value_low = value % 128
        return [
            0xF0,  # default
            0x00,  # default
            0x20,  # default
            0x32,  # default
            0x00,  # DEVICE ID: 00..0f
            0x0E,  # default
            0x20,  # FUNCTION
            0x01,  # FUNCTION
            channel,
            param,
            value_hi,
            value_low,
            0xF7  # default
        ]

    def enable_listen(self):
        command_to_listen = [0xF0, 0x00, 0x20, 0x32, 0x00, 0x0E, 0x3F, 0x04, 0x00, 0xF7]
        self.ser.write(serial.to_bytes(command_to_listen))
        time.sleep(0.1)

    def send_command(self, command_list):
        bytes_to_send = serial.to_bytes(command_list)
        self.ser.write(bytes_to_send)
        time.sleep(0.1)

    @staticmethod
    def convert_db(db):
        if db < -15 or db > 15:
            raise RuntimeError("Gain must be between -15 and +15 DB")
        db += 15
        return db * 10
