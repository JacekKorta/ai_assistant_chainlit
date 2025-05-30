import chainlit as cl
from openai import AsyncOpenAI
import os
import httpx

import chainlit_components
import config
from config.settings import get_settings


settings = get_settings()
client = AsyncOpenAI(api_key=settings.chainlit.proxy_api_key, base_url=settings.chainlit.proxy_api_url)

# Instrument the OpenAI client
cl.instrument_openai()



@cl.password_auth_callback
async def auth_callback(username: str, password: str):
    # Make HTTP request to Django backend to verify credentials
    response = None
    
    # Get the Django backend URL from environment variable or use default
    django_backend_url = os.environ.get("DJANGO_BACKEND_URL", "http://nginx")
    verify_credentials_url = f"{django_backend_url}/api/accounts/verify-credentials/"
    
    print(f"Attempting to authenticate with: {verify_credentials_url}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                verify_credentials_url,
                json={"username": username, "password": password},
                timeout=10.0
            )
    except httpx.ConnectError as e:
        # Connection refused, server not available
        print(f"Connection error: {str(e)}")
        return None
    except httpx.TimeoutException as e:
        # Request timed out
        print(f"Request timeout: {str(e)}")
        return None
    except httpx.RequestError as e:
        # Any other request-related error
        print(f"Request error: {str(e)}")
        return None
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected authentication error: {str(e)}")
        return None
        
    # Process the response outside the try/except block
    if response.status_code == 200:
        # Credentials are valid
        return cl.User(
            identifier=username, 
            metadata={"role": "user", "provider": "credentials"}
        )
    elif response.status_code == 401:
        # Unauthorized - invalid credentials
        print("Invalid credentials")
        return None
    else:
        # Other HTTP error
        print(f"Unexpected status code: {response.status_code}")
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
