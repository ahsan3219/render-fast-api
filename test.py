# import requests

# # Define the URL of the endpoint
# url = 'https://command-request.onrender.com/api/japanese'

# # Define the payload to be sent in the POST request
# payload = {"history": [
# {
# "message": "Hello, how can I assist you?",
# "type": "AI Message",
# "command": ""}
# ]



# }

# # Optionally, define headers
# headers = {
#     'Content-Type': 'application/json',
# }

# # Make the POST request
# response = requests.post(url, json=payload, headers=headers)

# # Check the status code of the response
# if response.status_code == 200:
#     print('Success:', response.json())
# else:
#     print('Failed:', response.status_code, response.text)



# import requests

# API_URL = "https://flowise-02i3.onrender.com/api/v1/prediction/1e03c376-f4a2-40b8-aeee-42a56243c88f"

# def query(payload):
#     response = requests.post(API_URL, json=payload)
#     return response.json()
    
# output = query({
#     "question": "Hey, how are you?",
#     "streaming":True
# })
# print(output)


import socketio
import requests
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the Socket.IO client
sio = socketio.Client(logger=True, engineio_logger=True)  # Set logger to True for debugging

@sio.event
def connect():
    print("Connected to Flowise server")
    query()

@sio.event
def connect_error(data):
    print(f"Connection error: {data}")

@sio.event
def disconnect():
    print("Disconnected from Flowise server")

@sio.on('start')
def on_start(data):
    print("Streaming started")

@sio.on('token')
def on_token(token):
    print(f"{token}", end='', flush=True)

@sio.on('end')
def on_end(data):
    print("\nStreaming ended")
    sio.disconnect()

@sio.on('sourceDocuments')
def on_source_documents(docs):
    print("\nSource Documents:", docs)

@sio.on('usedTools')
def on_used_tools(tools):
    print("\nUsed Tools:", tools)

@sio.on('nextAgent')
def on_next_agent(agent):
    print("\nNext Agent:", agent)

@sio.on('agentReasoning')
def on_agent_reasoning(reasoning):
    print("\nAgent Reasoning:", reasoning)

def query():
    url = "https://flowise-02i3.onrender.com/api/v1/prediction/1e03c376-f4a2-40b8-aeee-42a56243c88f"
    question = input("Please enter your question: ")
    data = {
        "question": question,
        "socketIOClientId": sio.sid,
        "stream": True
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print("Query sent. Waiting for response...")
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text[:100]}...")  # Print first 100 characters
    except requests.exceptions.RequestException as e:
        print(f"Error sending query: {e}")

if __name__ == '__main__':
    try:
        # Connect to the Socket.IO server
        sio.connect('https://flowise-02i3.onrender.com', transports=['websocket', 'polling'])
        
        # Set a timeout of 60 seconds
        timeout = time.time() + 60
        while time.time() < timeout:
            sio.sleep(1)
            if not sio.connected:
                break
        
        if sio.connected:
            print("Timeout reached. Disconnecting...")
            sio.disconnect()
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if sio.connected:
            sio.disconnect()
