import requests

# Define the URL of the endpoint
url = 'https://command-request.onrender.com/api/japanese'

# Define the payload to be sent in the POST request
payload = {"history": [
{
"message": "Hello, how can I assist you?",
"type": "AI Message",
"command": ""}
]



}

# Optionally, define headers
headers = {
    'Content-Type': 'application/json',
}

# Make the POST request
response = requests.post(url, json=payload, headers=headers)

# Check the status code of the response
if response.status_code == 200:
    print('Success:', response.json())
else:
    print('Failed:', response.status_code, response.text)
