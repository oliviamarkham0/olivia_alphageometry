import subprocess
import os
import time

'''
Uses DDAR to solve + output proofs and images(optional)
'''

def run_command_for_problem(problem_name, output_directory, real_one):
    problem_dir_path = os.path.join(output_directory, os.path.dirname(problem_name))
    os.makedirs(problem_dir_path, exist_ok=True)
    proof_output_path = os.path.join(problem_dir_path, f"{os.path.basename(problem_name)}.proof.txt")

    command = [
        "python3", "-m", "alphageometry",
        "--alsologtostderr",
        f"--problems_file={real_one}",
        f"--problem_name={problem_name}",
        "--mode=ddar",
        f"--out_file={proof_output_path}"
    ]

    print("Executing:", " ".join(command))
    
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=7)
        print(f"Processed problem {problem_name}, proof written to {proof_output_path}")
    except subprocess.TimeoutExpired:
        print(f"Timeout for problem {problem_name}. Skipping...")
    except subprocess.CalledProcessError as e:
        print(f"Error processing problem {problem_name}: {e}")
        print(e.output.decode())
        if os.path.exists(proof_output_path):
            os.remove(proof_output_path)

def main():
    start_time = time.time()
    problem_file = "full_problems.txt"
    output_directory = "xx"

    with open(problem_file, 'r') as f:
        while True:
            problem_name_line = f.readline().strip()
            if not problem_name_line:
                break
            run_command_for_problem(problem_name_line, output_directory, problem_file)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")
    
if __name__ == "__main__":
    main()