from typing import Optional
from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import asyncio
import concurrent.futures



load_dotenv()

Command_URL = os.getenv('Command_URL')
print("Command_URL", Command_URL)

Message_URL = os.getenv('Message_URL')
print("Message_URL", Message_URL)

Japanese_URL=os.getenv("Japanese_URL")
print("Japanese_URL", Japanese_URL)

Japanese_URL_Rem=os.getenv("Japanese_URL_Rem")
print("Japanese_URL_Rem", Japanese_URL_Rem)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def command_query(payload):
    response = requests.post(Command_URL, json=payload)
    return response.json()

def message_query(payload):
    response = requests.post(Message_URL, json=payload)
    return response.json()

def message_japanese_query(payload):
    response = requests.post(Japanese_URL, json=payload)
    return response.json()

def message_japanese_query_rem(payload):
    response = requests.post(Japanese_URL_Rem, json=payload)
    return response.json()

def clean_string(input_string):
    # Remove newline characters
    cleaned_string = input_string.replace('\n', '')
    
    # Remove leading space if it exists
    if cleaned_string.startswith(' '):
        cleaned_string = cleaned_string[1:]
    
    return cleaned_string


@app.post("/api/english")
# First Version Time Issue
# async def hello(request: Request):
#     body = await request.json()
    
#     history = body.get('history', [])
#     filtered_history = [
#     {
#         "message": entry["message"],
#         "type": entry["type"]
#     }
#     for entry in body["history"]
#     ]   
    
#     # print("History",filtered_history)
#     # Find the latest user message and command
#     latest_user_message = None
#     latest_command = None

#     for entry in reversed(history):
#         if entry.get("type") == "userMessage":
#             latest_user_message = entry.get("message")
#             latest_command = entry.get("command")
#             break

#     if latest_user_message is None:
#         return JSONResponse(content={"error": "No user message found in history"}, status_code=400)

#     res_command = command_query({"question": latest_user_message})
#     res_message = message_query({"question": latest_user_message,
#     "override":{
#     "memoryKey": filtered_history}})

#     command_res=clean_string(res_command.get("text"))
#     print("Command_res",command_res)
#     message_res=clean_string(res_message.get("text"))
#     print("message_res",message_res)

#     response={
#         'type': "AI Message",
#         'message': message_res,
#         'command': command_res
#     }
#     return JSONResponse(content={"response": response}, status_code=200)

# Second Version Fixed Time Issue
async def hello(request: Request):
    body = await request.json()
    history = body.get('history', [])
    
    filtered_history = [
        {
            "message": entry["message"],
            "type": entry["type"]
        }
        for entry in history
    ]

    latest_user_message = None
    latest_command = None

    for entry in reversed(history):
        if entry.get("type") == "userMessage":
            latest_user_message = entry.get("message")
            latest_command = entry.get("command")
            break

    if latest_user_message is None:
        return JSONResponse(content={"error": "No user message found in history"}, status_code=400)

    payload_command = {"question": latest_user_message}
    payload_message = {"question": latest_user_message, "history": filtered_history}

    # Run both queries concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_command = executor.submit(command_query, payload_command)
        future_message = executor.submit(message_query, payload_message)
        
        res_command = future_command.result()
        res_message = future_message.result()

    command_res = clean_string(res_command.get("text"))
    print("Command_res", command_res)
    message_res = clean_string(res_message.get("text"))
    print("message_res", message_res)

    response = {
        'type': "AI Message",
        'message': message_res,
        'command': command_res
    }

    return JSONResponse(content={"response": response}, status_code=200)




@app.post("/api/japanese")
# First Version Time taking
# async def hello(request: Request):
#     body = await request.json()
#     history = body.get('history', [])
    
#     history = body.get('history', [])
#     filtered_history = [
#     {
#         "message": entry["message"],
#         "type": entry["type"]
#     }
#     for entry in body["history"]
#     ]
#     # print("H`istory",filtered_history)

#     # Find the latest user message and command
#     latest_user_message = None
#     latest_command = None

#     for entry in reversed(history):
#         if entry.get("type") == "userMessage":
#             latest_user_message = entry.get("message")
#             latest_command = entry.get("command")
#             break

#     if latest_user_message is None:
#         return JSONResponse(content={"error": "No user message found in history"}, status_code=400)

#     res_command = command_query({"question": latest_user_message})
#     res_message = message_japanese_query({"question": latest_user_message,
#     "history": filtered_history})
    
#     command_res=clean_string(res_command.get("text"))
#     print("Command_res",command_res)
#     message_res=clean_string(res_message.get("text"))
#     print("message_res",message_res)

#     response={
#         'type': "AI Message",
#         'message': message_res,
#         'command': command_res
#     }
#     return JSONResponse(content={"response": response}, status_code=200)

# Second Version Fixed Time Issue
async def hello(request: Request):
    body = await request.json()
    history = body.get('history', [])
    
    filtered_history = [
        {
            "message": entry["message"],
            "type": entry["type"]
        }
        for entry in history
    ]

    latest_user_message = None
    latest_command = None

    for entry in reversed(history):
        if entry.get("type") == "userMessage":
            latest_user_message = entry.get("message")
            latest_command = entry.get("command")
            break

    if latest_user_message is None:
        return JSONResponse(content={"error": "No user message found in history"}, status_code=400)

    payload_command = {"question": latest_user_message}
    payload_message = {"question": latest_user_message, "history": filtered_history}

    # Run both queries concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_command = executor.submit(command_query, payload_command)
        future_message = executor.submit(message_japanese_query, payload_message)
        
        res_command = future_command.result()
        res_message = future_message.result()

    command_res = clean_string(res_command.get("text"))
    print("Command_res", command_res)
    message_res = clean_string(res_message.get("text"))
    print("message_res", message_res)

    response = {
        'type': "AI Message",
        'message': message_res,
        'command': command_res
    }

    return JSONResponse(content={"response": response}, status_code=200)



@app.post("/api/japanese/rem")
# First Version Taking Time To response
# async def hello(request: Request):
#     body = await request.json()
#     history = body.get('history', [])
    
#     history = body.get('history', [])
#     filtered_history = [
#     {
#         "message": entry["message"],
#         "type": entry["type"]
#     }
#     for entry in body["history"]
#     ]
#     # print("H`istory",filtered_history)

#     # Find the latest user message and command
#     latest_user_message = None
#     latest_command = None

#     for entry in reversed(history):
#         if entry.get("type") == "userMessage":
#             latest_user_message = entry.get("message")
#             latest_command = entry.get("command")
#             break

#     if latest_user_message is None:
#         return JSONResponse(content={"error": "No user message found in history"}, status_code=400)

#     res_command = command_query({"question": latest_user_message})
#     res_message = message_japanese_query_rem({"question": latest_user_message,
#     "history": filtered_history})

#     command_res=clean_string(res_command.get("text"))
#     print("Command_res",command_res)
#     message_res=clean_string(res_message.get("text"))
#     print("message_res",message_res)

#     response={
#         'type': "AI Message",
#         'message': message_res,
#         'command': command_res
#     }

#     return JSONResponse(content={"response": response}, status_code=200)
# Second Version Fixed Time Issue
async def hello(request: Request):
    body = await request.json()
    history = body.get('history', [])
    
    filtered_history = [
        {
            "message": entry["message"],
            "type": entry["type"]
        }
        for entry in history
    ]

    latest_user_message = None
    latest_command = None

    for entry in reversed(history):
        if entry.get("type") == "userMessage":
            latest_user_message = entry.get("message")
            latest_command = entry.get("command")
            break

    if latest_user_message is None:
        return JSONResponse(content={"error": "No user message found in history"}, status_code=400)

    payload_command = {"question": latest_user_message}
    payload_message = {"question": latest_user_message, "history": filtered_history}

    # Run both queries concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_command = executor.submit(command_query, payload_command)
        future_message = executor.submit(message_japanese_query_rem, payload_message)
        
        res_command = future_command.result()
        res_message = future_message.result()

    command_res = clean_string(res_command.get("text"))
    print("Command_res", command_res)
    message_res = clean_string(res_message.get("text"))
    print("message_res", message_res)

    response = {
        'type': "AI Message",
        'message': message_res,
        'command': command_res
    }

    return JSONResponse(content={"response": response}, status_code=200)


@app.get("/test")
def test():
    return {"message": "Test"}

@app.get("/result")
def result(request: Request):
    data = {'phy': 50, 'che': 60, 'maths': 70}
    return templates.TemplateResponse("result.html", {"request": request, "result": data})
