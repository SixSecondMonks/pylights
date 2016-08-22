from bibliopixel.animation import BaseStripAnim, BaseMatrixAnim
from audioop import rms
from math import log10
import pyaudio

RATE  = 44100
CHUNK = 1024

class AudioMixin(object):
    def __init__(self, device_index, led, start, end):
        super(AudioMixin, self).__init__(led, start, end)

        if device_index is None:
            raise ValueError('device_index is nil')

        self.device_index = device_index
        self.volume = 1
        self.decibels = 1

        def get_volume(data, frame_count, time_info, status):
            self.volume = max(1, rms(data, 2)) # always have 1 becuase log10(0) is invalid
            self.decibels = 20 * log10(self.volume)
            return (data, pyaudio.paContinue)

        self.py_audio = pyaudio.PyAudio()
        self.py_audio_stream = self.py_audio.open(format=pyaudio.paInt16, channels=1, input_device_index=self.device_index, rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=get_volume)
        self.py_audio_stream.start_stream()

class StripAnim(AudioMixin, BaseStripAnim):
    def __init__(self, device_index, led, start, end):
        super(StripAnim, self).__init__(device_index, led, start, end)

class MatrixAnim(BaseMatrixAnim, AudioMixin):
    pass
