from bibliopixel.animation import BaseStripAnim, BaseMatrixAnim
from audioop import rms
from math import log10
import pyaudio

RATE  = 44100
CHUNK = 1024

class AudioMixin(object):
    def __init__(self, led, start, end):
        super(AudioMixin, self).__init__(led, start, end)
        self.volume = 1
        self.decibels = 1

        def get_volume(data, frame_count, time_info, status):
            self.volume = rms(data, 2)
            self.decibels = 20 * log10(self.volume)
            return (data, pyaudio.paContinue)

        self.py_audio = pyaudio.PyAudio()
        self.py_audio_stream = self.py_audio.open(format=pyaudio.paInt16, channels=1, input_device_index=7, rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=get_volume)
        self.py_audio_stream.start_stream()

class StripAnim(AudioMixin, BaseStripAnim):
    def __init__(self, led, start, end):
        super(StripAnim, self).__init__(led, start, end)

class MatrixAnim(BaseMatrixAnim, AudioMixin):
    pass
