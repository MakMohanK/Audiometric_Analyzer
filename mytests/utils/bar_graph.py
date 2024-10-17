import matplotlib.pyplot as plt
import numpy as np

# Sample data
x_label = 'Category A'
y_values = [10, 10, 10, 20, 20, 20]  # Three values for the y-axis
labels = ['Value 1', 'Value 2', 'Value 3', 'Value 4', 'Value 5', 'Value 6']  # Labels for each bar

# Set positions for the bars
x_pos = np.arange(len(labels))

# Create a bar graph
plt.figure(figsize=(6, 4))
plt.bar(x_pos, y_values, color=['blue', 'orange', 'green'])

# Add titles and labels
plt.title('Bar Graph for One Category with Multiple Values')
plt.xlabel('Categories')
plt.ylabel('Values')

# Customize x-axis ticks
plt.xticks(x_pos, labels)

# Show grid lines
plt.grid(axis='y', linestyle='--', alpha=0.2)

# Display the bar graph
plt.show()
