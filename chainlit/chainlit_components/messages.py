import chainlit as cl
from openai import AsyncOpenAI



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