import os
import subprocess

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"ERROR: File not found: {path}"
    except Exception as e:
        return f"ERROR: Could not read file: {e}"

def write_file(path, content):
    try:
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to {path}"
    except Exception as e:
        return f"ERROR: Could not write file: {e}"

def list_files(directory="."):
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


# Test cases
if __name__ == "__main__":
    print(write_file("test.txt","hello world"))
    print(read_file("test.txt"))
    print(list_files("."))