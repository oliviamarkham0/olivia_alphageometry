import timeout_decorator
import os
import shutil
import dd
import graph as gh
import problem as pr

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

@timeout_decorator.timeout(3, timeout_exception=StopIteration)
def process_problem(key, defs, output_directory):
    p = problems[key]
    g, _ = gh.Graph.build_problem(p, defs)
    gh.nm.draw(
      g.type2nodes[gh.Point],
      g.type2nodes[gh.Line],
      g.type2nodes[gh.Circle],
      g.type2nodes[gh.Segment],
      save_to=f"{output_directory}/{key}.jpg")

problem_file = "tester3_full.txt"
# Load problems and reverse their order
problems = pr.Problem.from_txt_file(problem_file, to_dict=True, translate=False)
problems = dict(reversed(list(problems.items())))

output_directory = "./output7_problems"

# Ensure the output directory exists and is clear
ensure_directory_exists(output_directory)

defs = pr.Definition.from_txt_file('defs.txt', to_dict=True)

for key in problems:
    try:
        process_problem(key, defs, output_directory)
        print(f"Processed {key}")
    except StopIteration:
        print(f"Skipped {key} due to timeout")
