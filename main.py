from typing import Optional
from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import asyncio
import concurrent.futures
from fastapi.middleware.cors import CORSMiddleware
import uuid


load_dotenv()

session_histories = {}


Command_URL = os.getenv('Command_URL')
print("Command_URL", Command_URL)

Message_URL = os.getenv('Message_URL')
print("Message_URL", Message_URL)

Japanese_URL=os.getenv("Japanese_URL")
print("Japanese_URL", Japanese_URL)

Japanese_URL_Rem=os.getenv("Japanese_URL_Rem")
print("Japanese_URL_Rem", Japanese_URL_Rem)

# Second version Env start here

mai_english_message_url=os.getenv("mai_english_message_url")
print("mai_english_message_url", mai_english_message_url)

jesus_rag_url=os.getenv("jesus_rag_url")
print("jesus_rag_url", jesus_rag_url)

mai_japanese_message_url=os.getenv("mai_japanese_message_url")
print("mai_japanese_message_url", mai_japanese_message_url)

mai_spanish_message_url=os.getenv("mai_spanish_message_url")
print("mai_spanish_message_url", mai_spanish_message_url)

rem_english_message_url=os.getenv("rem_english_message_url")
print("rem_english_message_url", rem_english_message_url)

rem_japanese_message_url=os.getenv("rem_japanese_message_url")
print("rem_japanese_message_url", rem_japanese_message_url)

rem_spanish_message_url=os.getenv("rem_spanish_message_url")
print("rem_spanish_message_url", rem_spanish_message_url)


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


# Second Version for all six endpoints start here
def mai_english_message(payload):
    response = requests.post(mai_english_message_url, json=payload)
    return response.json()

def mai_japanese_message(payload):
    response = requests.post(mai_japanese_message_url, json=payload)
    return response.json()


def mai_spanish_message(payload):
    response = requests.post(mai_spanish_message_url, json=payload)
    return response.json()


def rem_english_message(payload):
    response = requests.post(rem_english_message_url, json=payload)
    return response.json()


def rem_japanese_message(payload):
    response = requests.post(rem_japanese_message_url, json=payload)
    return response.json()


def rem_spanish_message(payload):
    response = requests.post(rem_spanish_message_url, json=payload)
    return response.json()

def jesus_rag(payload):
    response = requests.post(jesus_rag_url, json=payload)
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



# Second version start from here it contains all six endpoints 27-june-2024
@app.post("/api/mai/english")
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
        future_message = executor.submit(mai_english_message, payload_message)
        
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


@app.post("/api/mai/japanese")
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
        future_message = executor.submit(mai_japanese_message, payload_message)
        
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


@app.post("/api/mai/spanish")
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
        future_message = executor.submit(mai_spanish_message, payload_message)
        
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


@app.post("/api/rem/english")
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
        future_message = executor.submit(rem_english_message, payload_message)
        
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


@app.post("/api/rem/japanese")
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
        future_message = executor.submit(rem_japanese_message, payload_message)
        
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


@app.post("/api/rem/spanish")
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
        future_message = executor.submit(rem_spanish_message, payload_message)
        
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




@app.post("/api/rag/jesuschirst")
async def hello(request: Request):
    body = await request.json()
    
    # Get or generate sessionId
    session_id = body.get('sessionId')
    print("Session Id", session_id)
    if not session_id:
        session_id = str(uuid.uuid4())
        session_histories[session_id] = []

    history = body.get('history', [])
    if session_id in session_histories:
        session_histories[session_id].extend(history)
    else:
        session_histories[session_id] = history

    filtered_history = [
        {
            "message": entry["message"],
            "type": entry["type"]
        }
        for entry in session_histories[session_id]
    ]

    latest_user_message = None

    for entry in reversed(session_histories[session_id]):
        if entry.get("type") == "userMessage":
            latest_user_message = entry.get("message")
            break

    if latest_user_message is None:
        raise HTTPException(status_code=400, detail="No user message found in history")

    if session_id:
        payload_message = {
            "question": latest_user_message,
            "history": filtered_history,
            "overrideConfig": {
                "sessionId": session_id
            }
        }
        print("Payload",payload_message)
    else:
        payload_message = {
            "question": latest_user_message,
            "history": filtered_history
        }
        print("Payload",payload_message)

    # Run both queries concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_message = executor.submit(jesus_rag, payload_message)
        res_message = future_message.result()
    message_res = clean_string(res_message.get("text"))

    response = {
        'type': "AI Message",
        'message': message_res,
        'sessionId': session_id  # Include sessionId in the response
    }

    return JSONResponse(content={"response": response}, status_code=200)


@app.get("/test")
def test():
    return {"message": "Test"}

@app.get("/")
def test():
    return {"message": "Greetings from ENDPOINTS MAIN PAGE"}


@app.get("/result")
def result(request: Request):
    data = {'phy': 50, 'che': 60, 'maths': 70}
    return templates.TemplateResponse("result.html", {"request": request, "result": data})
