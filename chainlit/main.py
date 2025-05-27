import chainlit as cl
from openai import AsyncOpenAI
import os

import chainlit_components
import config
from config.settings import get_settings


settings = get_settings()
litellm_proxy_url = os.environ.get("LITELLM_PROXY_URL")
if litellm_proxy_url:
    client = AsyncOpenAI(base_url=litellm_proxy_url, api_key="not-needed")
else:
    client = AsyncOpenAI(api_key=settings.openai.api_key)

# Instrument the OpenAI client
cl.instrument_openai()



@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None


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
