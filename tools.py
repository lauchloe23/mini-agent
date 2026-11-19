import os
import subprocess
import sys

# Only allow access to files inside the folder the agent was started in
def safe_path(path):
    full = os.path.normcase(os.path.realpath(path))
    root = os.path.normcase(os.path.realpath(os.getcwd()))
    return full if full == root or full.startswith(root + os.sep) else None

def read_file(path):
    full = safe_path(path)
    if not full:
        return f"ERROR: Access denied (outside project folder): {path}"
    try:
        with open(full, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"ERROR: File not found: {path}"
    except Exception as e:
        return f"ERROR: Could not read file: {e}"

def write_file(path, content):
    full = safe_path(path)
    if not full:
        return f"ERROR: Access denied (outside project folder): {path}"
    try:
        directory = os.path.dirname(full)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to {path}"
    except Exception as e:
        return f"ERROR: Could not write file: {e}"

def list_files(directory="."):
    directory = directory or "."
    if not safe_path(directory):
        return f"ERROR: Access denied (outside project folder): {directory}"
    file_list = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
        for filename in files:
            if filename.startswith("."):
                continue
            full_path = os.path.join(root, filename)
            file_list.append(full_path)
    return "\n".join(file_list) if file_list else "No files found"

# subprocess
def run_command(command):
    try:
        result = subprocess.run(
            command,
            shell = True,
            capture_output = True,
            text = True,
            timeout = 30,
        )
        output = result.stdout
        
        if result.stderr: 
            output += f"\n[stderr]: {result.stderr}"
        if not output.strip():
            output = f"(command finished with no output, exit code {result.returncode})"
        return output
    except subprocess.TimeoutExpired:
        return "ERROR: Command timed out after 30 seconds"
    except Exception as e:
        return f"ERROR: Could not run command: {e}"


def git_diff():
    try:
        result = subprocess.run(
            ["git", "diff"],
            capture_output = True,
            text = True,
            timeout = 30
        )
        if result.returncode != 0:
            return f"ERROR: git diff failed: {result.stderr}"
        output = result.stdout
        return output if output.strip() else "No uncommitted changes."
    except FileNotFoundError:
        return "ERROR: git is not installed or not on PATH."
    except subprocess.TimeoutExpired:
        return "ERROR: git diff timed out."
    except Exception as e:
        return f"ERROR: Could not run git diff: {e}"


def run_tests():
    try:
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-v"],
            capture_output = True,
            text = True,
            timeout = 60
        )
        status = "PASSED" if result.returncode == 0 else "FAILED"
        return f"Tests {status}.\n{result.stdout}{result.stderr}"
    except subprocess.TimeoutExpired:
        return "ERROR: tests timed out after 60 seconds."
    except Exception as e:
        return f"ERROR: Could not run tests: {e}"


# Test cases
if __name__ == "__main__":
    print(write_file("test.txt","hello world"))
    print(read_file("test.txt"))
    print(list_files("."))