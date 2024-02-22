import random
from itertools import permutations
from multiprocessing import Pool, cpu_count
import os

defs_file = 'defs.txt'
output_file = 'generated_premises_noparallelogram.txt'

INTERSECT = ['midpoint', 'on_aline', 'eqdistance', 'eqangle3', 'angle_bisector', 'eqangle2', 'excenter2', 'incenter', 'free', 'angle_mirror', 'on_line', 'on_circle', 'orthocenter', 'on_dia', 'on_pline', 'segment', 'circle', 'r_triangle', 'incenter2', 'triangle', 'on_bline', 'foot', 'iso_triangle', 'mirror', 'on_tline', 'reflect', 'cc_tangent']

def worker_task(args):
    depth, starting_points, definitions = args
    return explore_premises_randomly(depth, starting_points, definitions)

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
    return premise_name != 'on_circle' or 'circle' in current_premises

def get_new_point_name(existing_points):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    available_letters = set(alphabet) - set(existing_points)
    if available_letters:
        return min(available_letters)
    return None

def create_premises_dict(existing_premises):
    existing_premises_dict = {}
    for premise in existing_premises:
        _, premise_content = premise.split(' = ')
        premise_name, points = premise_content.split(' ', 1)
        existing_premises_dict.setdefault(premise_name, []).append(points.strip())
    return existing_premises_dict

def check_permutation_uniqueness(all_permutations, existing_premises_dict):
    for perm in all_permutations:
        for premise_name_new, points_list in existing_premises_dict.items():
            for lst in points_list:
                if all(element in lst for element in perm):
                    return False
    return True

def modify_points_for_premise(premise_name, points_used, definitions, existing_premises):
    unique_premise_generated = False
    premise_str = ""
    new_point = ""
    
    while not unique_premise_generated:
        new_point = get_new_point_name(set(points_used).union(existing_premises))
        points_used.add(new_point)
        
        if len(points_used) - 1 < len(definitions[premise_name]['points']) - 1:
            return None, points_used
        
        args = [new_point] + random.sample(list(points_used - {new_point}), len(definitions[premise_name]['points']) - 1)
        premise_str = f"{new_point} = {premise_name} {' '.join(args)}"
        
        if premise_str not in existing_premises:
            new_premise_str = f"{premise_name} {' '.join(args[1:])}"
            all_permutations = permutations(args[1:], len(args[1:]))
            existing_premises_dict = create_premises_dict(existing_premises)

            if check_permutation_uniqueness(all_permutations, existing_premises_dict):
                unique_premise_generated = True

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

def generate_random_premises_parallel(defs_file, depth, num_iterations, num_workers):
    definitions = load_premise_definitions(defs_file)
    args = [(depth - 1, set(['a', 'b', 'c']), definitions) for _ in range(num_iterations)]
    
    with Pool(processes=num_workers) as pool:
        for result in pool.imap_unordered(worker_task, args):
            current_premises = ['a b c = triangle a b c'] + result
            with open(output_file, 'a') as f:
                f.write('; '.join(current_premises) + '\n')

def main():
    depth = 13 #Number of premises in problem
    num_iterations = 10000000 #number of problems we want to generate
    num_workers = os.cpu_count()

    open(output_file, 'w').close()
    
    generate_random_premises_parallel(defs_file, depth, num_iterations, num_workers)

if __name__ == "__main__":
    main()