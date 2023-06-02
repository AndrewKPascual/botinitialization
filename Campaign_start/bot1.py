import requests
from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import json

API_URL = "http://localhost:3000/api/v1/prediction/b6af391e-a2b8-445d-b82a-139997284854"

app = Flask(__name__)
run_with_ngrok(app)  # Integrate ngrok with Flask app

# Define the function before using it
def run_question_answering(question):
    return f"Here is a response to the question: {question}"

summary = run_question_answering('say the name of the company first then, give a summary')
print(summary)

conversation_memory = []  # Define conversation_memory

@app.route('/', methods=['POST'])
def process_message():
    message = request.args.get('message')

    if not conversation_memory:
        initial_message = f"Here is the summary, {summary}. You will be talking about this."
        response = query({'question': initial_message})
        conversation_memory.append(initial_message)
        
        return jsonify({'message': 'It worked'})  # Return JSON response

    conversation_memory.append(message)
    response = query({'question': message})
    
    # check the response status code
    if response.status_code == 200:
        try:
            response_json = response.json()
            bot_message = response_json.get('message', 'Error: Invalid response from the API')
            return jsonify({'message': bot_message})
        except json.decoder.JSONDecodeError:
            response_text = response.text
            print(response_text)  # Print the response text for debugging
            return jsonify({'error': 'Invalid JSON response from the API'}), 500
    else:
        return jsonify({'error': 'Error response from the API'}), 500

@app.route('/query', methods=['POST'])
def call_query():
    # get the question parameter from the POST request
    question = request.args.get('question')
    
    # handle the case where the question parameter isn't provided
    if question is None:
        return jsonify({'error': 'No question provided'}), 400

    # send the POST request to the API
    response = query({'question': question})

    # check the response status code
    if response.status_code == 200:
        try:
            response_json = response.json()
            return jsonify(response_json)
        except json.decoder.JSONDecodeError:
            response_text = response.text
            print(response_text)  # Print the response text for debugging
            return jsonify({'error': 'Invalid JSON response from the API'}), 500
    else:
        return jsonify({'error': 'Error response from the API'}), 500

# Define the function before using it
def query(payload):
    response = requests.post(API_URL, json=payload)
    return response

if __name__ == '__main__':
    # Start ngrok tunnel
    from pyngrok import ngrok
    ngrok_url = ngrok.connect(5000).public_url
    print('Ngrok URL:', ngrok_url)
    app.run()
