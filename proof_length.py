import os
import matplotlib.pyplot as plt
import numpy as np

def get_proof_length(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # Assuming the proof length can be inferred from the lines, adjust as needed
        second_last_line = lines[-2].strip()
        proof_length = int(second_last_line.split('.')[0]) if '.' in second_last_line else 0
        return proof_length

directory = 'proof_outputs'

# Use a list of tuples to track both proof length and filename
proof_lengths_and_names = []

# Iterate over files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".proof.txt"):
        file_path = os.path.join(directory, filename)
        proof_length = get_proof_length(file_path)
        proof_lengths_and_names.append((proof_length, filename))

# Sort the list by proof length in descending order
proof_lengths_and_names.sort(reverse=True, key=lambda x: x[0])

# Extract just the lengths for the histogram
proof_lengths = [length for length, _ in proof_lengths_and_names]

max_length = max(proof_lengths) if proof_lengths else 0

bin_edges = np.arange(0.5, max_length + 1.5, 1)

plt.figure(figsize=(10, 6))

plt.hist(proof_lengths, bins=bin_edges, color='#5A9BD4', edgecolor='black', alpha=0.7, rwidth=0.8)
plt.xlabel('Proof Length', fontsize=12)
plt.ylabel('Count (log scale)', fontsize=12)
plt.title('Histogram of Proof Lengths', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(np.arange(1, max_length + 1, 1), fontsize=10)
plt.yticks(fontsize=10)

plt.yscale('log')

mean_proof_length = np.mean(proof_lengths) if proof_lengths else 0
plt.axvline(x=mean_proof_length, color='red', linestyle='--', linewidth=1, label='Mean')

plt.legend()
plt.tight_layout()
plt.show()

# Display the top 5 longest proofs
print("Top 5 Longest Proofs:")
for i, (length, name) in enumerate(proof_lengths_and_names[:5], start=1):
    print(f"{i}. {name} - Length: {length}")
