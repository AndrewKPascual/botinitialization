import requests
from flask import Flask, request
from questioner import run_question_answering
from flask_ngrok import run_with_ngrok
from pyngrok import ngrok

API_URL = "https://flowise.andrewpascual.repl.co/api/v1/prediction/1557b335-1881-407e-a486-879806f50e89"

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
    return {"message": response.text}  # Wrap the response string in a dictionary

if __name__ == '__main__':
    conversation_memory = []

    # Start ngrok tunnel
    ngrok_url = ngrok.connect(5000).public_url
    print('Ngrok URL:', ngrok_url)

    app.run()
