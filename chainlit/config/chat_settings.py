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
    models_items = {model["id"].split("/")[1]: model["id"] for model in models_response["data"]}
    if not models_items:
        models_items = {"gpt-4.1": "openai/gpt-4.1",
                         "gpt-4.1-nano": "openai/gpt-4.1-nano",
                         "gpt-4o-mini": "openai/gpt-4o-mini",
                         "gpt-4o": "openai/gpt-4o"}
        
    sorted_models_items = dict(sorted(models_items.items(), key=lambda x: x[0]))

    session_id = str(uuid.uuid4())
    cl.user_session.set("session_id", session_id)
    

    chat_settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Available Models",
                items=sorted_models_items,
                initial_value="openai/gpt-4o-mini" # todo: pozwolić skonfigurowac userowi lub wczytać z globalnego
            ),
        ]
    ).send()

@cl.on_settings_update
async def update_settings(new_settings):
    cl.user_session.set("chat_settings", new_settings)
    print("on_settings_update", new_settings)
