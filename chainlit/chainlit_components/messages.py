import chainlit as cl
from openai import AsyncOpenAI



@cl.on_chat_resume
async def on_chat_resume(thread):
    pass

@cl.on_message
async def on_message(message: cl.Message):
    # cl.chat_context.to_openai() - cała historia z kontekstu
    chat_settings = cl.user_session.get("chat_settings") or {}
    client: AsyncOpenAI = cl.user_session.get("client")

    message_history: list[dict] = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")

    stream = await client.chat.completions.create(
        messages=message_history,
        stream=True,
        model=chat_settings.get("Model", "gpt-4.1-nano"),
        temperature=chat_settings.get("Temperature", 1.0)
    )

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})

    await msg.update()