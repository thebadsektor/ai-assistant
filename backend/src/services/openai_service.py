from typing import AsyncGenerator
from ..config import Config
from openai import AsyncOpenAI
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

config = Config()
client = AsyncOpenAI(api_key=config.openai_api_key)

"""
Python does not allow return statements with a value in an asynchronous generator function. 
The generate_inference function is structured as an asynchronous generator due to the yield statements used for the streaming response. 
When streaming=False, this design causes a conflict because you're trying to return a value (all_content) in a context where only yield is permitted.

To resolve this, you need to fundamentally separate the streaming and non-streaming logic. 
You can achieve this by creating two distinct functions: one for handling streaming responses and another for non-streaming responses.
"""

async def generate_inference_streaming(message: str) -> AsyncGenerator[str, None]:
    """
    Asynchronously generates a streaming inference response from the OpenAI API.

    Args:
    message (str): The user message to be processed by the model.

    Yields:
    AsyncGenerator[str, None]: A generator that yields the model's response in chunks.

    The function uses a streaming response, which is useful for handling long responses
    or for applications where you want to start processing the response before it's fully complete.
    """
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant for the company Westframework, skilled in explaining "
                        "complex concepts in simple terms."
                    ),
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            stream=True,
        )
        async for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    except Exception as e:
        logger.error(f"Error in generate_inference_streaming: {e}")
        yield "An error occurred while processing your request."


async def generate_inference_non_streaming(message: str) -> str:
    """
    Asynchronously generates a non-streaming inference response from the OpenAI API.

    Args:
    message (str): The user message to be processed by the model.

    Returns:
    str: The complete response from the model.

    This function is suitable for applications that require the entire response at once.
    The response is not streamed and is returned after the complete processing of the user's message.
    """
    try:
        response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant for the company Westframework, skilled in explaining "
                    "complex concepts in simple terms."
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        stream=False,
        )
        if response.choices:
            return ''.join([choice.message.content for choice in response.choices])
        else:
            return "No response generated."
    except Exception as e:
        logger.error(f"Error in generate_inference_non_streaming: {e}")
        return "An error occurred while processing your request."



