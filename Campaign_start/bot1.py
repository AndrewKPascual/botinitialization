import requests
from flask import Flask, request
from flask_ngrok import run_with_ngrok
from questioner import run_question_answering
from pyngrok import ngrok

API_URL = "https://flowise.andrewpascual.repl.co/api/v1/prediction/298efec4-ba22-4ec2-b2a5-c4729c619af9"

app = Flask(__name__)
run_with_ngrok(app)  # Integrate ngrok with Flask app

summary = run_question_answering('say the name of the company first then, give a summary')
print(summary)

@app.route('/', methods=['GET'])
def process_message():
    message = request.args.get('message')

    if not conversation_memory:
        initial_message = f"Here is the summary, {summary}. You will be talking about this."
        conversation_memory.append(summary)

        return {'message': initial_message}

    conversation_memory.append(message)
    response = query({'question': message})
    bot_message = response['message']

    return {'message': bot_message}

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

if __name__ == '__main__':
    conversation_memory = []
    # Start ngrok tunnel
    ngrok_url = ngrok.connect(5000).public_url
    print('Ngrok URL:', ngrok_url)
    app.run()
