from fastapi import APIRouter, WebSocket
from ..services.openai_service import generate_inference

router = APIRouter()
connected_clients = set()

async def connect_client(websocket: WebSocket):
    """
    Accept a new WebSocket connection and add it to the set of connected clients.

    Args:
        websocket (WebSocket): The WebSocket connection to accept.
    """
    await websocket.accept()
    connected_clients.add(websocket)

async def disconnect_client(websocket: WebSocket):
    """
    Remove a WebSocket client from the set of connected clients and close the connection.

    Args:
        websocket (WebSocket): The WebSocket connection to close.
    """
    connected_clients.remove(websocket)
    await websocket.close()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for generating OpenAI API inferences.

    This endpoint accepts WebSocket connections, receives messages (queries),
    and sends back generated responses using OpenAI's GPT model.
    
    Args:
        websocket (WebSocket): The WebSocket connection for the current client.
    """
    await connect_client(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            async for text in generate_inference(message):
                await websocket.send_text(text)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await disconnect_client(websocket)
