# This program demonstrates how to write a program that calls an API
# when using an LLM whose main function is to generate text

# import modules
from openai import OpenAI

# specify ollama model
model = 'qwen3.5:4b'

# Configure the client to connect to Ollama's local API
# The request is sent to Ollama running on the local machine
client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key = 'ollama' # required, but not used
)

# Send a request to the LLM and get a response
# The messages list represents the conversation between the user and the LLM
response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": 'user', "content": 'Explain what an AI agent is in one sentence'
        },
    ],
)

# to display content from the response
print(response.choices[0].message.content)

# This is step 1
# Whenever you're building an agent, you need an LLM
# To use the LLM, you need to send a request and receive a response