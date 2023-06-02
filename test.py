import requests

API_URL = "http://localhost:3000/api/v1/prediction/b6af391e-a2b8-445d-b82a-139997284854"

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()
    
output = query({
    "question": "Hey, how are you?",
})



print(output)