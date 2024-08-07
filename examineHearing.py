import sqlite3
import threading
import time
import numpy as np
import pyaudio
import playSound
import matplotlib.pyplot as plt

EXAMINATION_DATABASE = './database/examination.db'

conn = sqlite3.connect(EXAMINATION_DATABASE)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS hearing_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                negative fifty INTEGER,
                negative forty five INTEGER,
                negative forty INTEGER,
                negative thirty five INTEGER,
                negative thirty INTEGER,
                negative twenty five INTEGER,
                negative twenty INTEGER)''')

conn.commit()

def examine(frequency, decibels, duration):
    print(f"Playing sound at {frequency} Hz, {decibels} dB for {duration} seconds.")
    playSound.play_sound(frequency, decibels, duration)
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

    return heard

words = [
    "bare",
    "flower",
    "knight",
    "see",
    "peace"
]

def hearing_test():
    """Conduct a hearing test with commonly misheard words."""
    print("Welcome to the Hearing Test!")
    score = 0

    for word in words:
        playSound.play_word(word)
        user_input = input(f"Type the word you heard: ").strip().lower()

        if user_input == word:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct word was '{word}'.")

    print(f"Your score: {score}/{len(words)}")

def askUserCanHear():
    print("Can you hear the sound? (yes/no)")
    # timer = threading.Timer(2.0)
    # timer.start()
    user_input = input()
    # timer.cancel()
    return user_input.strip() if user_input else None

def playAllFrequencies(username):
    frequencies = [140, 130, 120, 110, 100, 90, 80, 70, 60, 50, 40, 30, 20]
    decibel_levels = [-50, -45, -40, -35, -30, -25, -20]
    heard_frequencies = []
    min_frequency = 150

    for decibel in decibel_levels:
        for frequency in frequencies: 
            if frequency>=min_frequency:
                continue
            heard = examine(frequency, decibel, 1)
            if heard:
                min_frequency = frequency
            if not heard:
                break

        heard_frequencies.append(min_frequency)
    
        
    cur.execute('INSERT INTO hearing_results (username,negative fifty,negative forty five,negative forty,negative thirty five,negative thirty,negative twenty five,negative twenty) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (username, heard_frequencies[0], heard_frequencies[1], heard_frequencies[2], heard_frequencies[3], heard_frequencies[4], heard_frequencies[5], heard_frequencies[6]))
    conn.commit()

    d = np.array(decibel_levels)
    f = np.array(heard_frequencies)

    plt.scatter(d,f)
    plt.show()

playAllFrequencies("NirvaanZ")

conn.close()