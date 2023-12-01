from fastapi import APIRouter, WebSocket
from ..services.openai_service import generate_inference_streaming, generate_inference_non_streaming
# ... other imports
import json

router = APIRouter()

# A set to keep track of all connected WebSocket clients
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
    await connect_client(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            request_data = json.loads(message)
            query = request_data.get("query")
            is_streaming = request_data.get("is_streaming", False)

            if is_streaming:
                async for text in generate_inference_streaming(query):
                    await websocket.send_text(text)
            else:
                # Directly get and send the complete response for non-streaming
                response = await generate_inference_non_streaming(query)
                await websocket.send_text(response)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await disconnect_client(websocket)
