import chainlit as cl
from openai import AsyncOpenAI
import httpx
import os
import logging
import asyncio

import chainlit_components
import config
from config.settings import get_settings

# Skonfiguruj podstawowy logging (można to zrobić w bardziej zaawansowany sposób w konfiguracji aplikacji)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # Uzyskaj instancję loggera dla tego modułu

settings = get_settings()
client = AsyncOpenAI(api_key=settings.openai.api_key)

# Adres URL Twojego backendu Django
DJANGO_BACKEND_URL = os.environ.get("DJANGO_BACKEND_URL", "http://localhost:8080")
VERIFY_CREDENTIALS_ENDPOINT = f"{DJANGO_BACKEND_URL}/api/accounts/verify-credentials/"

# Instrument the OpenAI client
cl.instrument_openai()



# Konfiguracja klienta HTTP dla autoryzacji z zaawansowanymi ustawieniami
auth_http_client = httpx.AsyncClient(
    timeout=httpx.Timeout(
        connect=3.0,    # Timeout połączenia
        read=10.0,      # Timeout odczytu
        write=3.0,      # Timeout zapisu
        pool=2.0        # Timeout puli połączeń
    ),
    limits=httpx.Limits(
        max_connections=10,        # Maksymalna liczba połączeń
        max_keepalive_connections=5,  # Maksymalna liczba bezczynnych połączeń
        keepalive_expiry=30.0     # Czas wygaśnięcia bezczynnych połączeń w sekundach
    )
)

@cl.password_auth_callback
async def auth_callback(username: str, password: str):
    """
    Asynchronicznie weryfikuje dane logowania użytkownika 
    poprzez wywołanie endpointu API w backendzie Django.
    """
    try:
        logger.info(f"Attempting authentication for user: {username}")
        
        # Próbujemy wykonać żądanie - z automatycznymi ponownymi próbami
        for attempt in range(3):
            try:
                response = await auth_http_client.post(
                    VERIFY_CREDENTIALS_ENDPOINT,
                    json={"username": username, "password": password},
                    timeout=10.0
                )
                break  # Jeśli żądanie się powiodło, przerywamy pętlę
            except httpx.RequestError as e:
                if attempt < 2:  # Próbujemy ponownie, jeśli to nie była ostatnia próba
                    wait_time = 2 ** attempt  # Exponential backoff (1, 2, 4 sekundy)
                    logger.warning(f"Authentication attempt {attempt+1} failed: {str(e)}. Retrying in {wait_time}s")
                    await asyncio.sleep(wait_time)
                else:
                    # Ostatnia próba nie powiodła się
                    raise
        
        # Sprawdź odpowiedź z backendu Django
        if response.status_code == 200:
            # Uwierzytelnienie udane
            logger.info(f"Authentication successful for user: {username}")
            return cl.User(identifier=username, metadata={"provider": "django"}) 
        elif response.status_code == 401:
            # Niepoprawne dane logowania
            logger.warning(f"Authentication failed for user: {username} - Invalid credentials")
            return None
        else:
            # Inny błąd po stronie backendu
            logger.error(f"Error verifying credentials. Status: {response.status_code}, Response: {response.text}")
            return None

    except httpx.RequestError as exc:
        # Błąd połączenia lub inny błąd zapytania
        logger.error(f"HTTP request error while requesting {exc.request.url!r}: {exc}")
        return None
    except Exception as e:
        # Inne nieoczekiwane błędy
        logger.exception("An unexpected error occurred during authentication")
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





