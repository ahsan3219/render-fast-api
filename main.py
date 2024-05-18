# from typing import Optional

# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}


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

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def command_query(payload):
    response = requests.post(Command_URL, json=payload)
    return response.json()

def message_query(payload):
    response = requests.post(Message_URL, json=payload)
    return response.json()

# @app.post("/api")
# async def hello(request: Request):
#     body = await request.json()
#     history = body.get('history', [])
    
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
#     print("latest_user_message",latest_user_message)
#     res_command = command_query({"question": latest_user_message})
#     res_message = message_query({"question": latest_user_message})

#     response = {
#         'Type': "userMessage_response",
#         'Command': res_command.get("text"),
#         'Message': res_message.get("text")
#     }

#     return JSONResponse(content=response, status_code=200)


@app.post("/api")
async def hello(request: Request):
    body = await request.json()
    history = body.get('history', [])
    
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
    res_message = message_query({"question": latest_user_message})

    # Append new responses to the history
    history.append({
        'type': "AI Message",
        'message': res_message.get("text"),
        'command': latest_command
    })

    return JSONResponse(content={"history": history}, status_code=200)

@app.get("/test")
def test():
    return {"message": "Test"}

@app.get("/result")
def result(request: Request):
    data = {'phy': 50, 'che': 60, 'maths': 70}
    return templates.TemplateResponse("result.html", {"request": request, "result": data})
