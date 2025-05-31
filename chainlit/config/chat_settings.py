import aiohttp
import uuid

import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider


async def fetch_models(settings):
    print("settings:", settings)
    url = f"{settings.chainlit.proxy_api_url}/v1/models?return_wildcard_routes=false&include_model_access_groups=false"
    headers = {
        "accept": "application/json",
        "x-litellm-api-key": settings.chainlit.proxy_api_key,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            return await response.json()


async def start(settings):
    models_response = await fetch_models(settings)
    models = [model["id"] for model in models_response["data"]]
    if not models:
        models = ["gpt-4.1", "gpt-4.1-nano", "gpt-4o-mini"]

    session_id = str(uuid.uuid4())
    cl.user_session.set("session_id", session_id)
    

    chat_settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Available Models",
                values=models,
                initial_value="gpt-4o-mini" # todo: pozwolić skonfigurowac userowi lub wczytać z globalnego
            ),
            Slider(
                id="Temperature",
                label="OpenAI - Temperature",
                initial=1,
                min=0,
                max=2,
                step=0.1,
            ),
        ]
    ).send()

@cl.on_settings_update
async def update_settings(new_settings):
    cl.user_session.set("chat_settings", new_settings)
    print("on_settings_update", new_settings)
