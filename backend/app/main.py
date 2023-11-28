from typing import AsyncGenerator, NoReturn

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from openai import AsyncOpenAI
import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import Config
from .routes.websocket import router as websocket_router

load_dotenv()

config = Config()
app = FastAPI()

# Set up CORS middleware
origins = [
    "http://localhost:3000",
    "localhost:3000"
]

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the WebSocket router
app.include_router(websocket_router)

# client = AsyncOpenAI(api_key=config.openai_api_key)

# async def generate_inference(message: str) -> AsyncGenerator[str, None]:
#     """
#     OpenAI Response
#     """
#     response = await client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {
#                 "role": "system",
#                 "content": (
#                     "You are a helpful assistant for the company Westframework, skilled in explaining "
#                     "complex concepts in simple terms."
#                 ),
#             },
#             {
#                 "role": "user",
#                 "content": message,
#             },
#         ],
#         stream=True,
#     )

#     all_content = ""
#     async for chunk in response:
#         content = chunk.choices[0].delta.content
#         if content:
#             all_content += content
#             yield all_content

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket) -> NoReturn:
#     """
#     Websocket for AI responses
#     """
#     await websocket.accept()
#     while True:
#         message = await websocket.receive_text()
#         async for text in generate_inference(message):
#             await websocket.send_text(text)

# Mount the React build folder as a static files directory
app.mount("/",
          StaticFiles(directory="frontend/build", html=True),
          name="static")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
