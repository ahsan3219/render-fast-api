from typing import Optional
from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

load_dotenv()

Command_URL = os.getenv('Command_URL')
print("Command_URL", Command_URL)

Message_URL = os.getenv('Message_URL')
print("Message_URL", Message_URL)

Japanese_URL=os.getenv("Japanese_URL")
print("Japanese_URL", Japanese_URL)

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

@app.post("/api/english")
async def hello(request: Request):
    body = await request.json()
    
    history = body.get('history', [])
    filtered_history = [
    {
        "message": entry["message"],
        "type": entry["type"]
    }
    for entry in body["history"]
]   
    
    # print("History",filtered_history)
    # Find the latest user message and command
    latest_user_message = None
    latest_command = None

    for entry in reversed(history):
        if entry.get("type") == "userMessage":
            latest_user_message = entry.get("message")
            latest_command = entry.get("command")
            break

    if latest_user_message is None:
        return JSONResponse(content={"error": "No user message found in history"}, status_code=400)

    res_command = command_query({"question": latest_user_message})
    res_message = message_query({"question": latest_user_message,
    "override":{
    "memoryKey": filtered_history}})

    # Append new responses to the history
    # history.append({
    #     'type': "AI Message",
    #     'message': res_message.get("text"),
    #     'command': res_command.get("text")
    # })

    response={
        'type': "AI Message",
        'message': res_message.get("text"),
        'command': res_command.get("text")
    }
    return JSONResponse(content={"response": response}, status_code=200)



@app.post("/api/japanese")
async def hello(request: Request):
    body = await request.json()
    history = body.get('history', [])
    
    history = body.get('history', [])
    filtered_history = [
    {
        "message": entry["message"],
        "type": entry["type"]
    }
    for entry in body["history"]
]
    # print("History",filtered_history)

    # Find the latest user message and command
    latest_user_message = None
    latest_command = None

    for entry in reversed(history):
        if entry.get("type") == "userMessage":
            latest_user_message = entry.get("message")
            latest_command = entry.get("command")
            break

    if latest_user_message is None:
        return JSONResponse(content={"error": "No user message found in history"}, status_code=400)

    res_command = command_query({"question": latest_user_message})
    res_message = message_japanese_query({"question": latest_user_message,
    "history": filtered_history})

    # Append new responses to the history
    # history.append({
    #     'type': "AI Message",
    #     'message': res_message.get("text"),
    #     'command': res_command.get("text")
    # })

    response={
        'type': "AI Message",
        'message': res_message.get("text"),
        'command': res_command.get("text")
    }
    return JSONResponse(content={"response": response}, status_code=200)

@app.get("/test")
def test():
    return {"message": "Test"}

@app.get("/result")
def result(request: Request):
    data = {'phy': 50, 'che': 60, 'maths': 70}
    return templates.TemplateResponse("result.html", {"request": request, "result": data})
