# creating a context window for an llm

# import modules
from openai import OpenAI

# specify ollama llm
model = 'qwen3.5:4b'

# configure the client to connect to ollama's local api
# the request is sent to Ollama running on the local machine
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama' # required, but not used
)

# create an empty list to store conversation history
messages = []

# create while loop to allow user to continuously send messages
while True:
    
    # ask user to enter a message
    user_input = input('You: ')
    
    # check if user wants to end the conversation
    if user_input.strip().lower() in ('exit', 'quit'):
        break
    
    # add the user's messages to the conversation history
    messages.append(
        {
            'role': 'user', 'content': user_input
        }
    )
    
    
    # send conversation history to the llm and get a response
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    
    
    # extract the text content from the llm's response
    reply = response.choices[0].message.content
    
    # add the llm's reponse to the conversation history
    messages.append(
        {
            "role": 'assistant', "content": reply
        }
    )
    
    
    # display llm's reponse
    print(f'Bot: {reply}')