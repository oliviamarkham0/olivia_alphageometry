def select_unique_lines(input_file, output_file, num_lines):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    # Ensure not to exceed the total number of lines in the file
    selected_lines = lines[:min(num_lines, len(lines))]

    # Create a set to store unique lines
    unique_lines = set()

    with open(output_file, 'w') as outfile:
        for i, line in enumerate(selected_lines, 1):
            # Check if the line is not in the set of unique lines
            if line not in unique_lines:
                depth = line.count(';') + 1  # Counting depth based on number of semicolons
                outfile.write(f"{depth}/{i}\n{line}")
                # Add the line to the set of unique lines
                unique_lines.add(line)

if __name__ == "__main__":
    input_file = "tester2.txt"
    #input_file = "modified_output.txt"
    output_file = "tester3_full.txt"
    #output_file = "tester.txt"
    num_lines = 43018  # Selecting the first 1000 lines
    select_unique_lines(input_file, output_file, num_lines)
