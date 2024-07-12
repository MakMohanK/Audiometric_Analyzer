import numpy as np
import pyaudio

def play_sound(frequency, decibels, duration, sample_rate=44100):

    t = np.linspace(0, duration, int(sample_rate * duration), False)

    waveform = np.sin(frequency * 2 * np.pi * t)

    waveform *= (10**(decibels/20))

    waveform = np.clip(waveform, -1.0, 1.0)

    audio = (waveform * 32767).astype(np.int16)

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    output=True)

    audio_bytes = audio.tobytes()

    stream.write(audio_bytes)

    stream.stop_stream()
    stream.close()

    p.terminate()
