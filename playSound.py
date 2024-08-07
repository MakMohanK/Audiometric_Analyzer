import numpy as np
import sounddevice as sd
import math
import os
import gtts
import playsound
import tempfile

def play_sound(frequency, decibels, duration, sample_rate=44100):

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    note = np.sin(2 * np.pi * frequency * t)

    note *= ((103.523*(1.06853**(decibels)))-3.68348)/100

    sd.play(note, sample_rate)

    sd.wait()

def play_word(word):
    """Generate and play the audio for the given word."""
    tts = gtts.gTTS(word)
    
    # Create a temporary file to save the audio
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        temp_file_name = f"{temp_file.name}.mp3"
        tts.save(temp_file_name)
        playsound.playsound(temp_file_name)

play_word("flower")