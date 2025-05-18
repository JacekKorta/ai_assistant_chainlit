"""
OpenAI Service for Chainlit application.
Provides a robust HTTP client for OpenAI API with retries, timeouts, and connection pooling.
"""
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
import httpx
import logging
import tenacity
from typing import List, Dict, Any, Optional
from config.settings import get_settings

# Configure logger
logger = logging.getLogger(__name__)

class OpenAIService:
    """
    A service class for interacting with the OpenAI API.
    Implements robust HTTP client with retries, timeouts, and connection pooling.
    """
    
    def __init__(self):
        settings = get_settings()
        # Configure base transport with connection pooling
        transport = httpx.AsyncHTTPTransport(
            limits=httpx.Limits(
                max_connections=100,  # Maximum number of connections
                max_keepalive_connections=20,  # Maximum number of idle connections
                keepalive_expiry=30.0  # Timeout for idle connections in seconds
            )
        )
        
        # Configure httpx client with sensible defaults
        http_client = httpx.AsyncClient(
            transport=transport,
            timeout=httpx.Timeout(
                connect=5.0,    # Connection timeout
                read=30.0,      # Read timeout
                write=10.0,     # Write timeout
                pool=5.0        # Pool timeout
            ),
            limits=httpx.Limits(
                max_connections=100,
                max_keepalive_connections=20
            ),
            http2=True         # Enable HTTP/2 for better performance
        )
        
        # Initialize AsyncOpenAI client with custom HTTP client
        self.client = AsyncOpenAI(
            api_key=settings.openai.api_key,
            http_client=http_client,
            max_retries=3,      # Set max retries for transient errors
        )
    
    @tenacity.retry(
        retry=tenacity.retry_if_exception_type(
            (httpx.ConnectError, httpx.ReadTimeout, httpx.ConnectTimeout)
        ),
        wait=tenacity.wait_exponential(multiplier=1, min=2, max=10),
        stop=tenacity.stop_after_attempt(3),
        before_sleep=lambda retry_state: logger.warning(
            f"Retrying OpenAI API call: attempt {retry_state.attempt_number} after error: {retry_state.outcome.exception()}"
        )
    )
    async def create_chat_completion(
        self,
        messages: List[ChatCompletionMessageParam],
        model: str = "gpt-4.1-nano",
        temperature: float = 1.0,
        stream: bool = False,
        **kwargs
    ) -> ChatCompletion:
        """
        Create a chat completion with robust error handling and retries.
        
        Args:
            messages: List of chat messages in OpenAI format
            model: OpenAI model to use
            temperature: Temperature for response generation
            stream: Whether to stream responses
            **kwargs: Additional parameters to pass to the OpenAI API
            
        Returns:
            ChatCompletion: The response from OpenAI
            
        Raises:
            Exception: If the OpenAI API call fails after retries
        """
        try:
            logger.info(f"Creating chat completion with model: {model}")
            response = await self.client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=temperature,
                stream=stream,
                **kwargs
            )
            return response
        except Exception as e:
            logger.error(f"Error in OpenAI API call: {str(e)}")
            # Re-raise the exception after logging it
            raise
