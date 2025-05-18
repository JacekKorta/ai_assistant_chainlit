import chainlit as cl
from openai import AsyncOpenAI
import os
import logging
import asyncio

import chainlit_components
import config
from config.settings import get_settings
from services.auth_service import AuthService

# Skonfiguruj podstawowy logging (można to zrobić w bardziej zaawansowany sposób w konfiguracji aplikacji)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # Uzyskaj instancję loggera dla tego modułu

settings = get_settings()
client = AsyncOpenAI(api_key=settings.openai.api_key)

# Adres URL Twojego backendu Django
DJANGO_BACKEND_URL = os.environ.get("DJANGO_BACKEND_URL", "http://localhost:8080")

# Inicjalizacja serwisu autoryzacji
auth_service = AuthService(DJANGO_BACKEND_URL)

# Instrument the OpenAI client
cl.instrument_openai()

@cl.password_auth_callback
async def auth_callback(username: str, password: str):
    """
    Asynchronicznie weryfikuje dane logowania użytkownika 
    poprzez wywołanie endpointu API w backendzie Django.
    """
    # Deleguj proces uwierzytelniania do serwisu autoryzacji
    return await auth_service.verify_credentials(username, password)


@cl.on_chat_resume
async def on_chat_resume(thread):
    pass

@cl.on_stop
async def on_stop():
    """Cleanup resources when the app is stopping."""
    await auth_service.close()

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
    try:
        response = await client.chat.completions.create(
            messages=messages + cl.chat_context.to_openai(),
            model=chat_settings.get("Model", "gpt-4.1-nano"),
            temperature=chat_settings.get("Temperature", 1)
        )
        await cl.Message(content=response.choices[0].message.content).send()
    except Exception as e:
        error_message = f"Error generating response: {str(e)}"
        logger.error(error_message)
        await cl.Message(content=f"⚠️ {error_message}").send()





