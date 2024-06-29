import sqlite3
import threading
import time
import numpy as np
import pyaudio

EXAMINATION_DATABASE = './database//examination.db'

conn = sqlite3.connect(EXAMINATION_DATABASE)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS hearing_results
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT UNIQUE,
              frequency INTEGER,
              decibel INTEGER,
              heard INTEGER,
              timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

conn.commit()

def play_sound(frequency, volume, duration, sample_rate=44100):
    
    if not (0.0 <= volume <= 1.0):
        raise ValueError("Volume must be between 0.0 and 1.0")

    t = np.linspace(0, duration, int(sample_rate * duration), False)

    waveform = np.sin(frequency * 2 * np.pi * t)

    waveform *= volume

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

def examine(frequency, volume, duration):
    print(f"Playing sound at {frequency} Hz, {volume} dB for {duration} seconds.")
    play_sound(frequency, volume, duration)
    user_response = askUserCanHear()
    if user_response is None:
        heard = 0
    elif user_response.lower() == 'yes':
        heard = 1
    elif user_response.lower() == 'no':
        heard = 0
    else:
        print("Invalid response from user.")
        heard = 0

    c.execute("INSERT INTO hearing_results (frequency, decibel, heard) VALUES (?, ?, ?)",
              (frequency, volume, heard))
    conn.commit()

    return heard

def askUserCanHear():
    print("Can you hear the sound? (yes/no)")
    timer = threading.Timer(2.0)
    timer.start()
    user_input = input()
    timer.cancel()
    return user_input.strip() if user_input else None

def playAllFrequencies():
    frequencies = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140]
    decibel_levels = [10, 20, 30, 40, 50, 60]

    heard_frequencies = set()

    for decibel in decibel_levels:
        for frequency in frequencies:
            if frequency in heard_frequencies:
                continue
            heard = examine(frequency, decibel, 1)
            if heard:
                heard_frequencies.add(frequency)

        if heard_frequencies.issuperset(frequencies[:frequencies.index(min(heard_frequencies))]):
            break

playAllFrequencies()

conn.close()