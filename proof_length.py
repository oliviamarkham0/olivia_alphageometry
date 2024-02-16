import os
import matplotlib.pyplot as plt
import numpy as np

def get_proof_length(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        second_last_line = lines[-2].strip()
        proof_length = int(second_last_line.split('.')[0]) if '.' in second_last_line else 0
        return proof_length

# Directory containing proof files
directory = 'x_4k/13'

# List to store proof lengths and filenames
proof_lengths = []
file_names = []

# Iterate over files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".proof.txt"):
        file_path = os.path.join(directory, filename)
        proof_length = get_proof_length(file_path)
        proof_lengths.append(proof_length)
        file_names.append(filename)

# Plot histogram
plt.figure(figsize=(10, 6))  # Set figure size

plt.hist(proof_lengths, bins=30, color='#5A9BD4', edgecolor='black', alpha=0.7)  # Adjust color and transparency
plt.xlabel('Synthetic proof length', fontsize=12)  # Set x label and font size
plt.ylabel('Count (log scale)', fontsize=12)  # Set y label and font size
plt.title('Histogram of Proof Lengths', fontsize=14)  # Set title and font size
plt.grid(True, linestyle='--', alpha=0.5)  # Add grid lines with transparency
plt.xticks(np.arange(min(proof_lengths), max(proof_lengths) + 1, 1), fontsize=10)  # Set x ticks font size and integer values
plt.yticks(fontsize=10)  # Set y ticks font size

# Set y-axis scale to logarithmic
plt.yscale('log')

# Add a vertical line for the mean
mean_proof_length = np.mean(proof_lengths)
plt.axvline(x=mean_proof_length, color='red', linestyle='--', linewidth=1, label='Mean')  

plt.legend()  # Show legend
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()

# Get indices of top 5 longest proof lengths
top5_indices = sorted(range(len(proof_lengths)), key=lambda i: proof_lengths[i], reverse=True)[:5]

# Print filenames of the top 5 longest proof lengths
print("Top 5 longest proof lengths:")
for index in top5_indices:
    print(file_names[index])
