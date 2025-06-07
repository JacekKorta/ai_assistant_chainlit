from functools import partial

import chainlit as cl

import chainlit_components # noqa
import config # noqa
from config.settings import get_settings
from config.chat_settings import start


settings = get_settings()
cl.instrument_openai()


prepared_start = partial(start, settings)

cl.on_chat_start(prepared_start)

