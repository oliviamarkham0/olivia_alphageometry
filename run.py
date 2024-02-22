import subprocess
import os
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def sanitize_problem_name(problem_name):
    """Convert problem names into a filesystem-friendly format."""
    return problem_name.replace("/", "_")

def run_command_for_problem(problem_details, output_directory, problem_file):
    start_time = time.time()  # Start timer for this function
    
    problem_name, problem_description = problem_details
    safe_problem_name = sanitize_problem_name(problem_name)
    proof_output_path = os.path.join(output_directory, f"{safe_problem_name}.proof.txt")

    command = [
        "python3", "-m", "alphageometry",
        "--alsologtostderr",
        f"--problems_file={problem_file}",
        f"--problem_name={problem_name}",
        "--mode=ddar",
        f"--out_file={proof_output_path}"
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=5)
        if os.path.exists(proof_output_path) and os.path.getsize(proof_output_path) > 0:
            print(f"Processed problem {problem_name}, proof written to {proof_output_path}")
        else:
            if os.path.exists(proof_output_path):
                os.remove(proof_output_path)
    except subprocess.CalledProcessError as e:
        if os.path.exists(proof_output_path):
            os.remove(proof_output_path)

    end_time = time.time()  # End timer for this function
    print(f"Time taken for {problem_name}: {end_time - start_time:.2f} seconds")  # Print the time taken for this function

def main():
    start_time = time.time()  # Start timer for the entire operation
    problem_file = "full_problems.txt"
    output_directory = "x_proof_outputs"
    os.makedirs(output_directory, exist_ok=True)

    problem_details_list = []

    with open(problem_file, 'r') as f:
        while True:
            problem_name_line = f.readline().strip()
            problem_description_line = f.readline().strip()
            if not problem_name_line or not problem_description_line:
                break
            problem_details_list.append((problem_name_line, problem_description_line))

    max_workers = os.cpu_count()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_command_for_problem, problem_details, output_directory, problem_file) for problem_details in problem_details_list]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                print(f'Generated an exception: {exc}')

    end_time = time.time()  # End timer for the entire operation
    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")  # Print the total execution time
    
if __name__ == "__main__":
    main()
