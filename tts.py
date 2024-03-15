import torch
import sounddevice as sd
import time

language = 'ru'
model_id = 'ru_v3'
sample_rate = 48000
speaker = 'aidar'  # aidar, baya, kseniya, xenia, eugene, random
put_accent = True
put_yo = True
try:
    device = torch.device('cuda')
except Exception:
    device = torch.device('cpu')
model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model.to(device)


def va_speak(what: str):
    audio = model.apply_tts(text=what + '..',
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo)

    sd.play(audio, sample_rate)
    time.sleep((len(audio) / sample_rate) + 0.5)
    sd.stop()
