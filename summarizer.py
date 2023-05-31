import openai
import time
import os
from dotenv import load_dotenv
load_dotenv()

def summarize_text(file_path):
    # Initialize OpenAI API client
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Define the desired summary length
    summary_length = 300

    # Read the input text from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        input_text = file.read()

    # Split the text into smaller chunks
    chunked_text = split_text(input_text, max_tokens=2000)

    # Initialize conversation memory
    conversation_memory = [{'role': 'system', 'content': 'You are a helpful assistant.'}]

    # Process each chunk of text
    for i, chunk in enumerate(chunked_text):
        # Create a new conversation or extend an existing one
        if i == len(chunked_text) - 1:
            system_message = 'This is the last chunk. Generating the summary now.'
        else:
            system_message = 'There are more chunks. Please wait for the next response.'

        conversation_memory.append({'role': 'user', 'content': chunk})
        conversation_memory.append({'role': 'system', 'content': system_message})

        # Truncate or reduce the message lengths to fit within the model's maximum context length
        while len(conversation_memory) > 4 and len(' '.join(msg['content'] for msg in conversation_memory)) > 4096:
            conversation_memory.pop(1)

        # Create or continue the conversation using the chat completion
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=conversation_memory
        )

        # Retrieve the reply from OpenAI
        reply = response.choices[-1].message.get('content')

        # Update the conversation memory
        conversation_memory.append({'role': 'assistant', 'content': reply})

        # Wait for a few seconds between API calls to avoid rate limits
        time.sleep(2)

    # Extract the last summary from the conversation memory
    summary = conversation_memory[-1]['content']

    # Save the summary to a new text file
    with open('summary.txt', 'w', encoding='utf-8') as file:
        file.write(summary)
    return 'summary.txt'
def split_text(text, max_tokens):
    tokens = text.split()
    chunks = []
    current_chunk = ''

    for token in tokens:
        if len(current_chunk) + len(token) < max_tokens:
            current_chunk += token + ' '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = token + ' '

    # Append the last chunk
    chunks.append(current_chunk.strip())

    return chunks

# Example usage
