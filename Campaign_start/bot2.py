import requests
from flask import Flask, request
from flask_ngrok import run_with_ngrok

API_URL_BOT1 = "https://flowise.andrewpascual.repl.co/api/v1/prediction/39518212-0848-4a3b-9b2c-ef4bb6ab0dce"
API_URL_BOT2 = "https://flowise.andrewpascual.repl.co/api/v1/prediction/ABCDEF12-3456-7890-ABCD-EF0123456789"
headers = {"Authorization": "Bearer h5+Sf+70vGiMJenqWgoBi73Iheyvx/p55BAV5DzkXZs="}

app = Flask(__name__)
run_with_ngrok(app)  # Integrate ngrok with Flask app

@app.route('/', methods=['POST'])
def process_message():
    user_input = request.form['message']

    # Send user input to bot1 for processing
    response_bot1 = query(API_URL_BOT1, {"question": user_input})

    # Check if response from bot1 is acceptable
    if is_response_acceptable(response_bot1):
        # Ask bot2 for their opinion on the user response
        approval = query(API_URL_BOT2, {"question": user_input})
        
        if is_response_acceptable(approval):
            # Proceed to next question
            return "Response approved. Proceed to the next question."
        else:
            return "Response not approved by bot2."
    else:
        return "Response not approved by bot1."

def query(api_url, payload):
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()

def is_response_acceptable(response):
    # Implement your logic to check if the response is acceptable
    # Return True if acceptable, False otherwise
    return True

if __name__ == '__main__':
    app.run()
