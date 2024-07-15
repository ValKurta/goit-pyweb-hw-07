import subprocess
import os
import sys


def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        print(f"Error running {' '.join(command)}:")
        print(result.stderr)
        return False
    else:
        print(f"Output of {' '.join(command)}:")
        print(result.stdout)
        return True


if __name__ == "__main__":
    print("Installing dependencies...")
    if not run_command([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt']):
        sys.exit("Failed to install dependencies.")

    # Change working directory to ./sqlite
    os.chdir('./sqlite')

    scripts = ['create_db.py', 'fill_data.py', 'queries_run.py']

    for script in scripts:
        print(f"Running {script}...")
        if not run_command([sys.executable, script]):
            print(f"Failed to run {script}. Exiting.")
            break
        print(f"Finished running {script}\n")
