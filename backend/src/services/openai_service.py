from typing import AsyncGenerator
from ..config import Config
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

config = Config()
client = AsyncOpenAI(api_key=config.openai_api_key)

async def generate_inference(message: str) -> AsyncGenerator[str, None]:
    """
    Generate responses using OpenAI
    """
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant for the company Westframework, skilled in explaining."
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

    all_content = ""
    async for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            all_content += content
            yield all_content
