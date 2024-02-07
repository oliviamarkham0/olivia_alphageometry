from collections import deque

def generate_new_identifier(existing_ids):
    for char in 'abcdefghijklmnopqrstuvwxyz':
        if char not in existing_ids:
            return char
    return None

def update_formula_with_action(current_formula, action, existing_ids):
    action_type, *params = action.split()
    if action_type in {'circle', 'midpoint', 'on_circle', 'on_line', 'foot'}:
        # These actions require existing points and generate a new element
        new_id = generate_new_identifier(existing_ids)
        if not new_id:
            return None  # No new identifier available
        if action_type == 'circle' and 'r_triangle' not in current_formula:
            return None  # Cannot perform action without a triangle
        updated_action = f"{new_id} = {action}"
    else:
        # For r_triangle or other actions not specified
        updated_action = action
    
    return f"{current_formula}; {updated_action}" if current_formula else updated_action

def can_perform_action(current_formula, action):
    if 'on_circle' in action and 'circle' not in current_formula:
        return False
    # Add more dependency checks as needed
    return True

def bfs_generate_formulas(initial_state, actions, max_depth):
    queue = deque([(initial_state, 0, set(initial_state.replace('=', '').replace(' ', '')))])
    formulas = []

    while queue:
        current_formula, depth, existing_ids = queue.popleft()
        if depth == max_depth:
            continue
        for action in actions:
            if can_perform_action(current_formula, action):
                new_formula = update_formula_with_action(current_formula, action, existing_ids)
                if new_formula:
                    new_ids = existing_ids.union(set(new_formula.replace('=', '').replace(' ', '')))
                    formulas.append(new_formula)
                    queue.append((new_formula, depth + 1, new_ids))
    
    return formulas

def read_actions(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def write_formulas_to_file(formulas, output_file):
    with open(output_file, 'w') as file:
        for formula in formulas:
            file.write(formula + "\n")

if __name__ == "__main__":
    initial_state = "a b c = r_triangle a b c"
    actions = read_actions("list_of_actions.txt")
    max_depth = 2  # Adjust depth as needed
    formulas = bfs_generate_formulas(initial_state, actions, max_depth)
    write_formulas_to_file(formulas, "output3.txt")
