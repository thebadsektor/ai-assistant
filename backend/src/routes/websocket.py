from typing import NoReturn
from fastapi import APIRouter, WebSocket
from ..services.openai_service import generate_inference

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> NoReturn:
    """
    Websocket for AI responses
    """
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        async for text in generate_inference(message):
            await websocket.send_text(text)
