from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv
from pyngrok import ngrok
from questioner import run_question_answering
import sqlite3

load_dotenv()

# Set up your OpenAI API credentials
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

# Define the path to the SQLite database file
DB_FILE = "conversation_history.db"

# Create the conversation history table if it doesn't exist
with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS conversation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT
        )
    """)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['GET'])
def chat():
    # Get the current conversation memory from the request
    conversation_memory_str = request.args.get('messages')
    conversation_memory = conversation_memory_str.split(',') if conversation_memory_str else []

    summary = run_question_answering('say the name of the company first then, give a summary')

    if not conversation_memory:
        # Provide a default conversation message if the list is empty
        initial_message = '''You are an AI questionnaire bot questioning specific users that dropped a service. Your role is to collect feedback and creative criticism about''' + summary + ''' this is enough information do not ask for more.
        Please ask these questions to user once they are ready.
        You will not state all the questions at once.
        You will ask one question at a time and not state the ones after it until the user has given a proper response.
        You will not get off script once the questions start to be asked. You will only ask these three questions and here they are:

        Question 1: Why did you drop the service?

        Question 2: What can we do better?

        Question 3: Did our website look aesthetically pleasing?

        '''
        conversation_memory = [{'role': 'system', 'content': initial_message}]
    else:
        # Save the conversation memory to the database
        save_conversation_memory(conversation_memory)

    # Generate a response using OpenAI Chat API
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=conversation_memory,
        temperature=0.1  # Adjust the temperature value as desired
    )

    # Get the model's reply from the API response
    model_reply = response['choices'][0]['message']['content']

    # Add model's reply to the conversation memory
    conversation_memory.append({'role': 'user', 'content': model_reply})

    # Save the updated conversation memory to the database
    save_conversation_memory(conversation_memory)

    # Check if the user response contains creative criticism
    if not is_creative_criticism(model_reply):
        # Repeat the question and ask for creative criticism
        repeated_question = conversation_memory[-2]['content']
        repeated_question += '\n\nPlease provide a response in a creative critic and suggest what we should change.'
        conversation_memory[-2]['content'] = repeated_question

    return {'response': model_reply}


def is_creative_criticism(response):
    # Check if the response contains creative criticism
    # You can implement your own logic here to validate the response
    # For simplicity, this function just checks if the response is not empty
    return bool(response)


def save_conversation_memory(conversation_memory):
    # Save the conversation memory to the database
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM conversation_history")  # Clear the previous conversation history
        for message in conversation_memory:
            c.execute("INSERT INTO conversation_history (role, content) VALUES (?, ?)",
                      (message['role'], message['content']))


if __name__ == '__main__':
    # Start ngrok tunnel
    ngrok_url = ngrok.connect(5000).public_url
    print('Ngrok URL:', ngrok_url)

    # Run Flask app
    app.run()
