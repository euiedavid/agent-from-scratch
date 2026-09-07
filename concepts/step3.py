# Tool calling
# This works by providing the LLM with a description (schema) of the tools
# it is allowed to use. The model can then request a tool call when needed.


# Import modules
from openai import OpenAI
# Imports the OpenAI client, which can also be used to communicate
# with Ollama because Ollama provides an OpenAI-compatible API.

import json
# Imports Python's built-in JSON module.
# We use it to convert the tool arguments from a JSON string
# into a Python dictionary.


# Specify the Ollama LLM
model = 'qwen3.5:4b'
# Specifies the local Ollama model that will process our messages.


# Configure the client
client = OpenAI(
    base_url='http://localhost:11434/v1',
    # Tells the OpenAI client to send requests to Ollama's
    # local API instead of OpenAI's API.

    api_key='ollama'  # Required by the OpenAI client, but Ollama does not use it for authentication
)
# Creates the client that will communicate with the locally
# running Ollama server.


# Define the function/tool
def read_file(file_path):
    # Defines a Python function that reads the contents of a text file.
    # file_path is the path to the file that should be read.

    try:
        # Starts a block where we attempt to execute the file-reading code.

        with open(file_path, 'r', encoding="utf-8") as f:
            # Opens the specified file in read mode ('r').
            # encoding="utf-8" allows the program to correctly read
            # standard Unicode characters.
            # "as f" gives us a variable representing the opened file.

            return f.read()
            # Reads the entire file and returns its contents.

    except FileNotFoundError:
        # Handles the situation where the specified file does not exist.

        return f'Error: File {file_path} not found'
        # Returns an error message instead of stopping the program.


# Since we're not using a framework, we manually define the tool schema.
# A tool schema describes the tool to the LLM:
# - what the tool is called
# - what it does
# - what arguments it accepts


# Configure the tool schema
TOOL_SCHEMAS = [
    {
        "type": "function",
        # Specifies that this tool is a function.

        "function": {
            "name": "read_file",
            # The name the model uses when requesting this tool.

            "description": "Read a text file and return its contents.",
            # Explains to the model what this tool does.
            # This helps the model decide when it should use the tool.

            "parameters": {
                "type": "object",
                # The tool's arguments are provided as an object/dictionary.

                "properties": {
                    "file_path": {
                        "type": "string",
                        # Specifies that file_path must be a string.

                        "description": "Path of the file to read"
                        # Explains what the file_path argument represents.
                    },
                },

                "required": ["file_path"],
                # Tells the model that file_path must be provided
                # when calling this tool.
            },
        },
    },
]


# Create the initial conversation/message
messages = [
    {
        "role": "user",
        "content": "What is inside notes.txt? Summarize it in one line."
    },
]
# Creates the message history.
# The user asks the model to inspect notes.txt and summarize it.
#
# The model cannot directly read the file.
# Instead, it can request the read_file tool.


# Start the tool-calling loop
while True:
    # Keeps asking the model what to do until the model produces
    # a final answer without requesting another tool.

    response = client.chat.completions.create(
        model=model,
        # Specifies which Ollama model should process the request.

        messages=messages,
        # Sends the conversation history to the model.

        tools=TOOL_SCHEMAS,
        # Sends the available tool definitions/schema to the model.
        # This tells the model that it has access to read_file().
    )
    
    # start of the loop

    message = response.choices[0].message
    # Extracts the model's message from the API response.

    # Inspect what the tool calls look like
    # print(message)
    # Prints the model's response so we can see whether it requested
    # a tool and what arguments it provided.

    messages.append(message)
    # Adds the model's message to the conversation history.
    # This is important because the next API request needs to know
    # what the model previously requested.


    # No tool calls means the model is done and gave us a normal answer
    if not message.tool_calls:
        # Checks whether the model requested any tools.
        # If there are no tool calls, the model has produced its
        # final response.

        print(message.content)
        # Prints the model's final answer.

        break
        # Stops the while loop because the task is finished.


    # Process each tool call requested by the model
    for tool_call in message.tool_calls:
        # Loops through every tool the model requested.
        # A model can potentially request multiple tools.

        args = json.loads(tool_call.function.arguments)
        # The model's tool arguments are returned as a JSON string.
        # json.loads() converts that JSON string into a Python dictionary.
        #
        # Example:
        # '{"file_path": "notes.txt"}'
        #
        # becomes:
        # {"file_path": "notes.txt"}

        print(f'Model wants to run: read_file({args})')
        # Shows us which tool the model wants to run
        # and which arguments it provided.


        result = read_file(**args)
        # Actually executes our Python function.
        #
        # **args unpacks the dictionary into keyword arguments.
        #
        # For example:
        # args = {"file_path": "notes.txt"}
        #
        # becomes:
        # read_file(file_path="notes.txt")


        messages.append(
            {
                "role": "tool",
                # Identifies this message as the result of a tool execution.

                "tool_call_id": tool_call.id,
                # Connects this tool result to the specific tool call
                # made by the model.

                "content": result,
                # Sends the file contents (or error message) back to the model.
            }
        )
        # Adds the tool result to the conversation history.
        #
        # The loop then goes back to the top, and the model receives
        # the tool result so it can generate the final answer.
        
    # display what the messages list actually looks like
    print(messages)
    # end of the loop
    