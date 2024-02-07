def unique_name(existing_names, base_name, original_names):
    if base_name not in existing_names and base_name not in original_names:
        return base_name
    i = 1
    new_name = f"{base_name}{i}"
    while new_name in existing_names or new_name in original_names:
        i += 1
        new_name = f"{base_name}{i}"
    return new_name

def process_line(line):
    parts = line.split('; ')
    existing_names = set(parts[0].split(' = ')[0].split())  # Initial shape names
    updated_formulas = []
    action_counts = {}  # Track occurrences of actions to ensure uniqueness

    for part in parts:
        name, rest = part.split(' = ', 1)
        action, *points = rest.split()

        # Generate a key to track action occurrences
        action_key = f"{action}_" + "_".join(sorted(points))
        action_counts[action_key] = action_counts.get(action_key, 0) + 1

        if action_counts[action_key] > 1:  # Skip or modify duplicate actions
            # Optionally modify the action here to make it unique
            continue  # Or modify the points list for the action

        if action == 'segment':
            new_points = [unique_name(existing_names, p, set()) for p in points]
            for p in new_points:
                existing_names.add(p)
            updated_action = f"{' '.join(new_points)} = {action} {' '.join(new_points)}"
        else:
            new_name = unique_name(existing_names, name, set())
            existing_names.add(new_name)
            if action in {'midpoint', 'on_line', 'foot', 'on_circle', 'orthocenter', 'circle', 'mirror'} and len(points) > 0:
                # Use new_name for the action's subject and keep other points as is
                updated_action = f"{new_name} = {action} {' '.join(points)}"
            else:
                updated_action = f"{new_name} = {rest}"
        updated_formulas.append(updated_action)

    return '; '.join(updated_formulas)


def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            updated_line = process_line(line.strip())
            outfile.write(updated_line + "\n")

if __name__ == "__main__":
    input_file = "output3.txt"
    output_file = "modified_output.txt"
    process_file(input_file, output_file)
