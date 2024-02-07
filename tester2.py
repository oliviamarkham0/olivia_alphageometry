import subprocess
import timeout_decorator
import os
import shutil
import problem as pr

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        clear_directory(directory)

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

@timeout_decorator.timeout(5, timeout_exception=StopIteration)
def process_problem(key, problems_file, defs, output_directory):
    command = [
        'python', '-m', 'alphageometry',
        '--alsologtostderr',
        f'--problems_file={problems_file}',
        f'--problem_name={key}',
        '--mode=alphageometry',
        # Add additional arguments here as needed
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        solution_output = result.stdout  # Capturing stdout where the solution is assumed to be

        # Writing the solution to a file
        with open(os.path.join(output_directory, f"{key}_solution.txt"), 'w') as sol_file:
            sol_file.write(solution_output)
        print(f"Processed and saved solution for {key}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {key}: {e}")

if __name__ == "__main__":
    problem_file = "tester3_full.txt"
    problems = pr.Problem.from_txt_file(problem_file, to_dict=True, translate=False)
    problems = dict(reversed(list(problems.items())))

    output_directory = "./output_problems"
    ensure_directory_exists(output_directory)

    defs = pr.Definition.from_txt_file('defs.txt', to_dict=True)

    for key in problems:
        try:
            process_problem(key, problem_file, defs, output_directory)
        except StopIteration:
            print(f"Skipped {key} due to timeout")
