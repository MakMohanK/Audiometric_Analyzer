import numpy as np
import pyaudio

def play_sound(frequency, decibels, duration=1.0, sample_rate=44100):
    
    # Generate the time values
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # Generate the waveform
    waveform = np.sin(frequency * 2 * np.pi * t)

    # Adjust waveform amplitude
    waveform *= ((103.523*(1.06853**(decibels)))-3.68348)/100

    # Ensure that the waveform is in the range -1.0 to 1.0
    waveform = np.clip(waveform, -1.0, 1.0)

    # Convert waveform to 16-bit PCM format
    audio = (waveform * 32767).astype(np.int16)

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    output=True)

    # Convert the audio to bytes
    audio_bytes = audio.tobytes()

    # Play the sound by writing the audio data to the stream
    stream.write(audio_bytes)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate PyAudio
    p.terminate()

# def play_word(word):
#     """Generate and play the audio for the given word."""
#     tts = gtts.gTTS(word)
    
#     # Create a temporary file to save the audio
#     with tempfile.NamedTemporaryFile(delete=True) as temp_file:
#         temp_file_name = f"{temp_file.name}.mp3"
#         tts.save(temp_file_name)
#         playsound.playsound(temp_file_name)

# play_word("flower")