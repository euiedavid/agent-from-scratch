# agentic-ai-from-scratch

This project is intended to practice and understand what happens under the hood when building an AI agent. The project uses Python and Ollama, with the LLM running locally through Ollama using the Qwen 3.5:4B model.

The project also demonstrates my understanding of how to build an agentic AI system from scratch without relying on agent frameworks.

This project follows the YouTube tutorial **"How to Build an AI Agent From Scratch in Python (No Frameworks)"** by Tech With Tim. The approximately 38-minute tutorial covers the fundamental concepts involved in building an AI agent, including what an agent is and the core steps involved in creating one.

The tutorial was used as a learning resource to understand the fundamentals of agent architecture and tool calling. This repository is my implementation and learning project based on the concepts presented in the tutorial.

This project is not intended to claim ownership of the original tutorial or its ideas. Credit for the original concept and tutorial goes to Tech With Tim.

While following the tutorial, I made several modifications to the code to better suit my intended use case and to ensure that the implementation works correctly with my local Ollama setup.

## Features

* Runs an LLM locally using Ollama
* Uses the Qwen 3.5:4B model
* Uses the OpenAI-compatible Python client to communicate with Ollama
* Implements an AI agent without an agent framework
* Supports tool calling
* Lists files and directories
* Reads text files
* Creates and overwrites text files
* Runs Windows CMD commands
* Requests user approval before executing shell commands
* Handles tool errors and returns them to the agent
* Maintains conversation history during the agent session
* Allows the agent to perform multiple tool calls to complete a task

## Tools

The agent currently has four tools:

### `list_files`

Lists the files and directories in a specified path.

### `read_file`

Reads and returns the contents of a text file.

### `write_file`

Creates a new text file or overwrites an existing text file with the provided content.

### `run_command`

Executes a Windows CMD command after asking the user for approval.

For example, the agent can use this tool to create a directory:

```text
mkdir snake_game
```

The user is asked to approve the command before it is executed.

## Technologies Used

* **Python** — Main programming language
* **Ollama** — Runs the LLM locally
* **Qwen 3.5:4B** — Local LLM used by the agent
* **OpenAI Python Client** — Used to communicate with Ollama's OpenAI-compatible API
* **JSON** — Used to process tool-call arguments
* **Subprocess** — Used to execute Windows CMD commands
* **Git & GitHub** — Version control and project repository

## How to Run

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd agents-from-scratch
```

### 2. Create and activate a virtual environment

On Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### 3. Install the required package

Install the OpenAI Python client:

```bash
pip install openai
```

### 4. Install Ollama

Install Ollama and make sure it is running on your computer.

### 5. Download the Qwen model

Pull the model using:

```bash
ollama pull qwen3.5:4b
```

### 6. Run the agent

```bash
python agent.py
```

You should see:

```text
Mini agent ready. Type 'exit' to quit.
```

You can then enter a request for the agent.

For example:

```text
You: Create a folder called snake_game
```

The agent can determine that it needs to use the `run_command` tool and ask for your approval before executing the command.

### 7. Exit the agent

Type:

```text
exit
```

or:

```text
quit
```

## Project Structure

```text
agents-from-scratch/
│
├── SnakeGame/
│   ├── constants.py
│   ├── game_functions.py
│   ├── main.py
│   └── requirements.txt
│
├── concepts/
│   ├── notes.txt
│   ├── step1.py
│   ├── step2.py
│   └── step3.py
│
├── agent.py
├── README.md
└── .gitignore
```

## Learning Objectives

This project was created to understand the core mechanics behind AI agents without relying on frameworks.

Through this project, I explored:

* How an LLM interacts with tools
* How tool schemas are provided to an LLM
* How an agent determines when to use a tool
* How tool arguments are passed as JSON
* How tool results are returned to the LLM
* How an agent can continue reasoning after receiving a tool result
* How conversation history is maintained
* How local LLMs can be integrated into agentic applications

## Attribution

This project was developed as a learning project based on the concepts demonstrated in Tech With Tim's **"How to Build an AI Agent From Scratch in Python (No Frameworks)"** tutorial.

The original tutorial and its concepts belong to Tech With Tim. This repository is an independent implementation created for educational and learning purposes, with modifications made for use with a local Ollama setup.