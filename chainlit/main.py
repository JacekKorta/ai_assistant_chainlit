from functools import partial

import chainlit as cl
from openai import AsyncOpenAI

import chainlit_components
import config
from config.settings import get_settings
from config.chat_settings import start

settings = get_settings()
client = AsyncOpenAI(api_key=settings.chainlit.proxy_api_key, base_url=settings.chainlit.proxy_api_url)

# Instrument the OpenAI client
cl.instrument_openai()


prepared_start = partial(start, settings)

cl.on_chat_start(prepared_start)

@cl.on_chat_resume
async def on_chat_resume(thread):
    pass

@cl.on_message
async def on_message(message: cl.Message):
    # cl.chat_context.to_openai() - cała historia z kontekstu
    chat_settings = cl.user_session.get("chat_settings") or {}
    messages=[
        {
            "content": "You are a helpful assistant",
            "role": "system"
        },  
    ]
    response = await client.chat.completions.create(
        messages=messages + cl.chat_context.to_openai(),
        model=chat_settings.get("Model", "gpt-4.1-nano"),
        temperature=chat_settings.get("Temperature", 1)
    )
    await cl.Message(content=response.choices[0].message.content).send()
