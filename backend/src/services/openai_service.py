from typing import AsyncGenerator
from ..config import Config
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

config = Config()
client = AsyncOpenAI(api_key=config.openai_api_key)

async def generate_inference_streaming(message: str) -> AsyncGenerator[str, None]:
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

async def generate_inference_non_streaming(message: str) -> str:
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
        # Concatenate text from all choices
        all_content = ''.join([choice.message.content for choice in response.choices])
        return all_content
    else:
        return "No response generated."



