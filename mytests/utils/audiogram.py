import numpy as np
import matplotlib.pyplot as plt

# Sample responses
responses = [
    {'frequency': 20, 'decibel': -45, 'response': 'No'},
    {'frequency': 20, 'decibel': -40, 'response': 'No'},
    {'frequency': 20, 'decibel': -35, 'response': 'No'},
    {'frequency': 30, 'decibel': -45, 'response': 'No'},
    {'frequency': 30, 'decibel': -40, 'response': 'No'},
    {'frequency': 30, 'decibel': -35, 'response': 'Yes'},
    {'frequency': 40, 'decibel': -45, 'response': 'Yes'},
    {'frequency': 40, 'decibel': -40, 'response': 'Yes'},
    {'frequency': 40, 'decibel': -35, 'response': 'Yes'},
    {'frequency': 50, 'decibel': -45, 'response': 'Yes'},
    {'frequency': 50, 'decibel': -40, 'response': 'Yes'},
    {'frequency': 50, 'decibel': -35, 'response': 'Yes'},
    {'frequency': 12000, 'decibel': -45, 'response': 'No'},
    {'frequency': 12000, 'decibel': -40, 'response': 'No'},
    {'frequency': 12000, 'decibel': -35, 'response': 'No'},
    {'frequency': 12500, 'decibel': -45, 'response': 'No'},
    {'frequency': 12500, 'decibel': -40, 'response': 'No'},
    {'frequency': 12500, 'decibel': -35, 'response': 'No'},
    {'frequency': 13000, 'decibel': -45, 'response': 'No'},
    {'frequency': 13000, 'decibel': -40, 'response': 'No'},
    {'frequency': 13000, 'decibel': -35, 'response': 'No'},
    {'frequency': 13500, 'decibel': -45, 'response': 'No'},
    {'frequency': 13500, 'decibel': -40, 'response': 'No'},
    {'frequency': 13500, 'decibel': -35, 'response': 'No'},
    {'frequency': 14000, 'decibel': -45, 'response': 'No'},
    {'frequency': 14000, 'decibel': -40, 'response': 'No'},
    {'frequency': 14000, 'decibel': -35, 'response': 'No'},
    {'frequency': 14500, 'decibel': -45, 'response': 'No'},
    {'frequency': 14500, 'decibel': -40, 'response': 'No'},
    {'frequency': 14500, 'decibel': -35, 'response': 'No'},
    {'frequency': 15000, 'decibel': -45, 'response': 'No'},
    {'frequency': 15000, 'decibel': -40, 'response': 'No'},
    {'frequency': 15000, 'decibel': -35, 'response': 'No'},
    {'frequency': 15500, 'decibel': -45, 'response': 'No'},
    {'frequency': 15500, 'decibel': -40, 'response': 'No'},
    {'frequency': 15500, 'decibel': -35, 'response': 'No'},
    {'frequency': 16000, 'decibel': -45, 'response': 'No'},
    {'frequency': 16000, 'decibel': -40, 'response': 'No'},
    {'frequency': 16000, 'decibel': -35, 'response': 'No'},
    {'frequency': 16500, 'decibel': -45, 'response': 'No'},
    {'frequency': 16500, 'decibel': -40, 'response': 'No'},
    {'frequency': 16500, 'decibel': -35, 'response': 'No'},
    {'frequency': 17000, 'decibel': -45, 'response': 'No'},
    {'frequency': 17000, 'decibel': -40, 'response': 'No'},
    {'frequency': 17000, 'decibel': -35, 'response': 'No'},
    {'frequency': 17500, 'decibel': -45, 'response': 'No'},
    {'frequency': 17500, 'decibel': -40, 'response': 'No'},
    {'frequency': 17500, 'decibel': -35, 'response': 'No'},
    {'frequency': 18000, 'decibel': -45, 'response': 'No'},
    {'frequency': 18000, 'decibel': -40, 'response': 'No'},
    {'frequency': 18000, 'decibel': -35, 'response': 'No'}
]

# Extract frequencies and decibels from responses
freqs = [entry['frequency'] for entry in responses if 20 <= entry['frequency'] <= 50 or 12000 <= entry['frequency'] <= 18000]
dBs = [entry['decibel'] for entry in responses if 20 <= entry['frequency'] <= 50 or 12000 <= entry['frequency'] <= 18000]

# Create frequency range
freq_range1 = np.arange(20, 51, 10)  # 20Hz to 50Hz
freq_range2 = np.arange(12000, 18001, 500)  # 12kHz to 18kHz
all_freqs = np.concatenate((freq_range1, freq_range2))

# Create a scatter plot
plt.figure(figsize=(10, 6))

# Plot the data points
plt.scatter(freqs, dBs, color='blue', label='Responses')

# Set x and y limits
plt.xlim(15, 18000)  # Set x-axis limits
plt.ylim(-45, -35)  # Set y-axis limits

# Set x-ticks to include all frequencies
plt.xticks(all_freqs, rotation=45)

# Labeling the graph
plt.title('Hearing Response Scatter Plot')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Decibel Level (dB)')
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')  # 0 dB line
plt.grid(True)

# Add legend
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
