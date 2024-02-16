from problem import Problem, Definition, Theorem, EmptyDependency
from graph import Graph
from dd import bfs_one_level
from timeout_decorator import timeout, TimeoutError

def format_dependency(dep):
    dep_str = dep.name + " " + " ".join([getattr(arg, 'name', str(arg)) for arg in dep.args])
    return dep_str.replace(", ", " ")

@timeout(5)
def process_problem(input_line, defs_file, theorems_file):
    problem = Problem.from_txt(input_line)
    definitions = Definition.from_txt_file(defs_file, to_dict=True)
    theorems = Theorem.from_txt_file(theorems_file, to_dict=True)
    graph, dependencies = Graph.build_problem(problem, definitions, verbose=False)
    added, derives, eq4s, branching = bfs_one_level(graph, theorems, 100, problem)
    return added

input_path = 'generated_premises.txt'
output_file = 'full_problems.txt'
defs_file = 'defs.txt'
theorems_file = 'rules.txt'

g_count = 0
b_count = 0

with open(input_path, 'r') as file:
    input_lines = [line.strip() for line in file.readlines()]
    
with open(output_file, 'w') as f_out:
    for input_line in input_lines:
        try:
            added = process_problem(input_line, defs_file, theorems_file)
        except (TimeoutError, AssertionError) as e:
            b_count += 1
            continue
        if not added:
            b_count += 1
        for i, dep in enumerate(added, start=1):
            print(f"Added {dep}")
            g_count += 1
            dep_str = format_dependency(dep)
            output_line = f"{input_line} ? {dep_str}"
            depth = output_line.count(';') + 1
            f_out.write(f"{depth}/{i}\n{output_line}\n")
        
print("Processing Complete")
print(f"Good count: {g_count}\nBad count: {b_count}")