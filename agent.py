# coding agent that has the ff tools:
# list_files
# read_file
# write_file
# run_command

# import modules
from openai import OpenAI
import json
import os
import subprocess

# specify the local Ollama model
model = 'qwen3.5:4b'

# OpenAI client configured to use Ollama's local API
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'  # placeholder; Ollama doesn't use this key locally
)

# system instructions given to the LLM
SYSTEM_PROMPT = """
You are a coding agent running in the user's terminal.
You can list files, read files, write files, and run shell commands.
Use your tools to complete the user's task, then briefly summarize what you did.
The working directory is the folder the user launched you from.

You are running on Windows.
Use Windows CMD commands, not Unix/Linux commands.
"""

# actual Python tool implementations

def list_files(path="."):
    entries = []

    # scandir provides file/folder entries from the given path
    for entry in os.scandir(path):
        # append "/" to directory names for easier identification
        entries.append(entry.name + ("/" if entry.is_dir() else ""))

    # return sorted entries as one string for the LLM
    return "\n".join(sorted(entries)) or "(empty directory)"


def read_file(file_path):
    # open file in read mode with UTF-8 encoding
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(file_path, content):
    # "w" creates the file or overwrites an existing file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    # return a result the LLM can use in the next turn
    return f"Saved {file_path} ({len(content)} characters)"
    
    
def run_command(command):
    # require user approval before executing a shell command
    answer = input(f"  Run '{command}'? [y/N]")

    if answer.strip().lower() != "y":
        return "The user declined to run this command."
    
    # explicitly execute the command through Windows CMD
    result = subprocess.run(
        ["cmd", "/c", command],
        capture_output=True,  # capture stdout/stderr for the LLM
        text=True,             # return output as strings
        timeout=120             # prevent indefinitely running commands
    )
    
    # combine normal output and error output
    output = (result.stdout + result.stderr).strip()

    # return command output or the exit code if there is no output
    return output or f'(no output, exit code {result.returncode})'


# maps tool names from the LLM to actual Python functions
TOOLS = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "run_command": run_command,
}


# tool schemas describe the available tools to the LLM
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List the files in a directory. Folders end with /.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory to list, e.g. '.'"
                    },
                },
                "required": ['path']
            },
        },
    },
    
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a text file and return its contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path of the file to read."
                    },
                },
                "required": ['file_path'],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create or overwrite a text file with the given content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path of the file to write"
                    },
                    "content": {
                        "type": "string",
                        "description": "Full contents of the file"
                    },
                },
                "required": ['file_path', 'content'],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a Windows CMD command and return its output. The user approves it first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The Windows CMD command to run"
                    },
                },
                "required": ['command']
            },
        },
    },
]


# executes the tool requested by the LLM
def run_tool(tool_call):
    # extract tool name from the model's tool call
    name = tool_call.function.name

    # convert JSON arguments into a Python dictionary
    args = json.loads(tool_call.function.arguments)

    # show which tool the agent selected
    print(f"  tool: {name}({args})")
 
    # return errors to the LLM instead of crashing the agent
    try:
        # look up the function and unpack the arguments
        return str(TOOLS[name](**args))
    
    except Exception as error:
        return f"Error: {error}"
    

# handles the agent's reasoning/tool-calling loop
def run_agent(messages):
    while True:
        # send conversation + tool definitions to the LLM
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOL_SCHEMAS,
        )
        
        # extract the assistant's response
        message = response.choices[0].message

        # preserve the assistant message in conversation history
        messages.append(message)
        
        # no tool calls = model has finished its task
        if not message.tool_calls:
            return message.content
        
        # execute every tool requested by the model
        for tool_call in message.tool_calls:
            result = run_tool(tool_call)

            # send the tool result back to the LLM
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })
            

# program entry point
def main():
    # initialize conversation with the system prompt
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("Mini agent ready. Type 'exit' to quit.")
    
    while True:
        # get the next user request
        user_input = input("\nYou: ")

        # stop the agent when requested
        if user_input.strip().lower() in ('exit', 'quit'):
            break
        
        # add user input to conversation history
        messages.append({
            "role": 'user',
            "content": user_input
        })

        # run the agent loop and get its final response
        reply = run_agent(messages)

        print(f"\nAgent: {reply}")
        
# only run main() when this file is executed directly
if __name__ == "__main__":
    main()