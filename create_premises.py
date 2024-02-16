import random
from itertools import permutations
defs_file = 'defs.txt'

INTERSECT = ['on_circle', 'on_line', 'midpoint', 'r_triangle', 'triangle', 'circle', 'foot', 'eq_triangle', 'on_tline', 'on_aline', 'on_bline', 'angle_bisector']

def load_premise_definitions(filename=defs_file):
    definitions = {}
    with open(filename, 'r') as file:
        content = file.read().strip()
        blocks = content.split('\n\n')
        for block in blocks:
            lines = block.strip().split('\n')
            premise = lines[0].split()
            name, points = premise[0], premise[1:]
            definitions[name] = {'name': name, 'points': points}
    return definitions

def can_use_premise(premise_name, current_premises):
    if premise_name == 'on_circle':
        if 'circle' not in current_premises:
            return False
    return True

def get_new_point_name(existing_points):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for letter in alphabet:
        if letter not in existing_points:
            return letter
    for first in alphabet:
        for second in alphabet:
            candidate = f"{first}{second}"
            if candidate not in existing_points:
                return candidate
    return None

def modify_points_for_premise(premise_name, points_used, definitions, existing_premises):
    unique_premise_generated = False
    premise_str = ""
    new_point = ""
    
    while not unique_premise_generated:
        if premise_name in INTERSECT:
            # Generate a new unique name for the intersect type which is not an existing point
            new_point = get_new_point_name(set(points_used).union(existing_premises))
            points_used.add(new_point)
            
            if len(points_used) - 1 < len(definitions[premise_name]['points']) - 1:
                return None, points_used
            
            # Select random points from existing ones for arguments, excluding the new point
            args = [new_point] + random.sample(list(points_used - {new_point}), len(definitions[premise_name]['points']) - 1)
            premise_str = f"{new_point} = {premise_name} {' '.join(args)}"
        
        # Ensure the generated premise is unique and hasn't been used before
        if premise_str not in existing_premises:
            new_premise_str = f"{premise_name} {' '.join(args[1:])}"
            if premise_name in INTERSECT:
                all_permutations = permutations(args[1:], len(args[1:]))
                #print(f"POINTS: {args[1:]}")
                existing_premises_dict = {}
                for premise in existing_premises:
                    parts = premise.split(' = ')
                    premise_name = parts[1].split()[0] 
                    points = ' '.join(parts[1].split()[1:]) 
                    if premise_name not in existing_premises_dict:
                        existing_premises_dict[premise_name] = [] 
                    existing_premises_dict[premise_name].append(points) 

                #print(existing_premises_dict)
                #print('ALL PERMUTATIONS:')
                for perm in all_permutations:
                    #print(perm)
                    #print(existing_premises_dict)
                    for premise_name_new, points_list in existing_premises_dict.items():
                        #print(f"POINTS LIST: {points_list}")
                        for lst in points_list:
                            #print(f'LST: {lst}')
                            if all(element in lst for element in perm):
                                #print(f"The points {perm} are in the premise type '{premise_name_new}'.")
                                unique_premise_generated = False
                                break
            else:
                new_premise_str = f"{premise_name} {' '.join(args[1:])}"
                if new_premise_str not in existing_premises:
                    unique_premise_generated = True
                    existing_premises.add(premise_str)

            if new_premise_str not in existing_premises:
                unique_premise_generated = True
            existing_premises.add(premise_str)
    
    return premise_str, points_used


def explore_premises_randomly(depth, points_used, definitions):
    existing_premises = set()
    current_premises = []

    while len(current_premises) < depth:
        premise_name = random.choice(INTERSECT)
        if can_use_premise(premise_name, current_premises):
            premise_format, updated_points_used = modify_points_for_premise(premise_name, points_used.copy(), definitions, existing_premises)
            if premise_format:
                current_premises.append(premise_format)
                points_used = updated_points_used.copy() 
    return current_premises

def generate_random_premises(defs_file, depth, num_iterations):
    definitions = load_premise_definitions(defs_file)
    premises_lists = []

    for _ in range(num_iterations):
        starting_points = set(['a', 'b', 'c'])
        current_premises = ['a b c = triangle a b c'] #Our starting premise (can be changed)
        random_premises = explore_premises_randomly(depth - 1, starting_points, definitions)
        full_premises = current_premises + random_premises
        premises_lists.append(full_premises)

    return premises_lists


def main():
    depth = 5 #Number of premises in problem
    num_iterations = 10000 #number of problems we want to generate
    premises_lists = generate_random_premises(defs_file, depth, num_iterations)
    output_file = 'generated_premises.txt'

    with open(output_file, 'w') as f:
        for premises in premises_lists:
            f.write('; '.join(premises) + '\n')

if __name__ == "__main__":
    main()
