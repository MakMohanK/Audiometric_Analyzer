
import numpy as np
import pyaudio

def play_sound(frequency, duration, volume):
    p = pyaudio.PyAudio()
    
    # Parameters
    fs = 44100       # Sampling rate, or number of samples per second
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)  # Time vector
    
    # Generate sound wave
    wave = (volume * np.sin(2 * np.pi * frequency * t)).astype(np.float32)
    
    # Open audio stream
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)
    
    # Play sound
    stream.write(wave.tobytes())
    
    # Close stream
    stream.stop_stream()
    stream.close()
    p.terminate()

# Example usage:
play_sound(frequency=180, duration=2, volume=0.28) 