import os

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

# Test cases
if __name__ == "__main__":
    print(write_file("test.txt","hello world"))
    print(read_file("test.txt"))
    print(list_files("."))