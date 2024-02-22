from multiprocessing import Pool, cpu_count
from problem import Problem, Definition, Theorem, EmptyDependency
from graph import Graph
from dd import bfs_one_level
from timeout_decorator import timeout, TimeoutError
from time import time
import os
import cProfile
import pstats
import traceback

input_path = 'generated_premises_noparallelogram.txt'
output_file = 'full_problems2.txt'
defs_file = 'defs.txt'
theorems_file = 'rules.txt'

def format_dependency(dep):
    dep_str = dep.name + " " + " ".join([getattr(arg, 'name', str(arg)) for arg in dep.args])
    return dep_str.replace(", ", " ")

@timeout(5)
def process_problem(args):
    input_line, defs_file, theorems_file = args
    problem = Problem.from_txt(input_line)
    definitions = Definition.from_txt_file(defs_file, to_dict=True)
    theorems = Theorem.from_txt_file(theorems_file, to_dict=True)
    graph, dependencies = Graph.build_problem(problem, definitions, verbose=False)
    added, derives, eq4s, branching = bfs_one_level(graph, theorems, 1000, problem)
    return input_line, added

def process_input_line(input_line):
    try:
        result = process_problem((input_line, defs_file, theorems_file))
        return result
    except Exception as e:
        #print(f"Error processing line: {input_line} | Error: {str(e)}")
        return None

def process_batch(batch):
    results = []
    with Pool(processes=cpu_count()) as pool:
        async_results = [pool.apply_async(process_input_line, (line,), callback=results.append) for line in batch]
        for async_result in async_results:
            async_result.wait()
            
    return [result for result in results if result is not None]

def normalize_line(segment):
    return ''.join(sorted(segment))

def normalize_angle(points):
    if len(points) % 2 != 0:
        return None
    #group points into line segments
    segments = [points[i:i+2] for i in range(0, len(points), 2)]
    normalized_segments = [normalize_line(segment) for segment in segments]
    sorted_segments = sorted(normalized_segments, key=lambda x: (x[0], x[1]))
    normalized_points = [point for segment in sorted_segments for point in segment]
    return normalized_points
    
def check_unique(dep, added_deps):
    parts = dep.split(' ')
    dep_type = parts[0]
    points = parts[1:]
    
    normalized_points = normalize_angle(points)
    if normalized_points is None:
        return False
    normalized_dep = f"{dep_type} {' '.join(normalized_points)}"
    if normalized_dep in added_deps:
        return False
    else:
        added_deps.append(normalized_dep)
    return True

def write_results(results, global_counter):
    with open(output_file, 'a') as f_out:
        for input_line, added in results:
            added_deps = []
            if added is not None:
                for dep in added:
                    dep_str = format_dependency(dep)
                    status = check_unique(dep_str, added_deps)
                    if status:
                        output_line = f"{input_line} ? {dep_str}"
                        depth = output_line.count(';') + 1
                        f_out.write(f"{depth}/{global_counter[0]}\n{output_line}\n")
                        global_counter[0] += 1
                        #print(f"ADDED LINE {depth}: {output_line}\n")

def process_in_batches(input_lines, batch_size=5):
    global_counter = [1]
    for i in range(0, len(input_lines), batch_size):
        batch = input_lines[i:i + batch_size]
        results = process_batch(batch)
        write_results(results, global_counter)

def main():
    open(output_file, 'w').close()

    with open(input_path, 'r') as file:
        input_lines = [line.strip() for line in file.readlines()]

    process_in_batches(input_lines)

    print("Processing Complete")

if __name__ == "__main__":
    cProfile.run('main()', 'profile_output.txt')