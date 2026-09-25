import json
from groq import Groq
from tools import read_file, write_file, list_files, run_command

# read GROQ_API_KEY from environment 
client = Groq()

MODEL = "openai/gpt-oss-20b"

TOOLS = [
    {
        "type" : "function",
        "function" : {
            "name" : "read_file",
            "description" : "Read the contents of a file at the given path and reutrn it as text.",
            "parameters" :{
                "type" : "object",
                "properties" : {
                    "path" : {
                        "type" : "string",
                        "description" : "Relative or absolute path to the file to read."
                    }
                },
                "required" : ["path"]
            }
        }
    },
    {
        "type" : "function",
        "function" : {
            "name" : "write_file",
            "description" : "Write text content to a file, overwriting it if it exists.",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "path" : {"type" : "string", "description" : "Path to file to write."},
                    "content" : {"type" : "string", "description" : "The full text content to write."}
                },
                "required" : ["path", "content"]
            }
        }
    },
    {
        "type" : "function",
        "function" : {
            "name" : "list_files",
            "description" : "List every file inside a directory, including subfolders.",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "directory" : {"type" : "string", "description" : "Directory to list. Defaults to current."}
                },
                "required" : []
            }
        }
    },
    {
        "type" : "function",
        "function": {
            "name" : "run_command",
            "description" : "Run a shell command on user's computer and return its output. Use this to run scripts, check tool versions, or run tests.",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "command" : {
                        "type" : "string",
                        "description" : "The exact shell command to run, e.g. 'ls -la' or 'python script.py'."
                    }
                },
                "required" : ["command"]
            }
        }
    }
]


# Function
def call_tool(name, arguments):
    if name == "read_file" :
        return read_file(arguments["path"])
    elif name == "write_file" : 
        return write_file(arguments["path"], arguments["content"])
    elif name == "list_files" :
        return list_files(arguments.get("directory", "."))
    elif name == "run_command" :
        command = arguments["command"]
        print(f"\n The agent wants to run this command:\n   {command}")
        approval = input("Do you approve? (y/n): ").strip().lower()
        if approval != "y":
            return "ERROR: User denied permission to run this command."
        return run_command(command)
    else:
        return f"ERROR: Unknown tool '{name}'"

def run_agent(user_message, conversation_history):
    conversation_history.append({"role" : "user", "content" : user_message})

    while True:
        response = client.chat.completions.create(
            model = MODEL,
            messages = conversation_history,
            tools = TOOLS,
        )

        message = response.choices[0].message
        conversation_history.append(message)

        if message.content:
            print(f"\nAgent: {message.content}")

        if not message.tool_calls:
            break

        for tool_call in message.tool_calls:
            name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f" [Running tool: {name}({arguments})]")
            result = call_tool(name, arguments)

            conversation_history.append({
                "role" : "tool",
                "tool_call_id" : tool_call.id,
                "content" : result,
            })
    return conversation_history

# Main Function
def main():
    print("Mini Coding Agent (V1) - type 'exit' to quit")
    conversation_history = []
    while True:
        user_message = input("\nYou: ")
        if user_message.strip().lower() == "exit":
            break
        conversation_history = run_agent(user_message, conversation_history)

if __name__ == "__main__":
    main()