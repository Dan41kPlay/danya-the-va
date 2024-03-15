import queue
import sys

import sounddevice as sd
import vosk
from ujson import loads

model = vosk.Model("model_small")
samplerate = 16000
device = 0

q = queue.Queue()


def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def va_listen():
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            while not rec.AcceptWaveform(q.get()):
                pass
            yield loads(rec.Result())['text']


if __name__ == '__main__':
    print('Listening...!')
    for phrase in va_listen():
        print(phrase)
