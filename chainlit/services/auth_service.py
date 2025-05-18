"""
Auth Service for Chainlit application.
Provides authentication functionality for Chainlit, communicating with Django backend.
"""
import httpx
import logging
import asyncio
from typing import Optional
import chainlit as cl

# Configure logger
logger = logging.getLogger(__name__)

class AuthService:
    """
    Service for handling authentication with Django backend.
    Implements robust HTTP client with retries and proper error handling.
    """
    
    def __init__(self, backend_url: str):
        """
        Initialize AuthService with backend URL.
        
        Args:
            backend_url: Base URL of the backend API
        """
        self.verify_credentials_endpoint = f"{backend_url}/api/accounts/verify-credentials/"
        
        # Configure persistent HTTP client with sensible defaults
        self.http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(
                connect=3.0,    # Connection timeout
                read=10.0,      # Read timeout
                write=3.0,      # Write timeout
                pool=2.0        # Pool timeout
            ),
            limits=httpx.Limits(
                max_connections=10,        # Maximum number of connections
                max_keepalive_connections=5,  # Maximum number of idle connections
                keepalive_expiry=30.0     # Timeout for idle connections in seconds
            )
        )
    
    async def verify_credentials(self, username: str, password: str) -> Optional[cl.User]:
        """
        Verify user credentials with Django backend.
        
        Args:
            username: Username to verify
            password: Password to verify
            
        Returns:
            cl.User if credentials are valid, None otherwise
        """
        try:
            logger.info(f"Attempting authentication for user: {username}")
            
            # Try request with automatic retries
            for attempt in range(3):
                try:
                    response = await self.http_client.post(
                        self.verify_credentials_endpoint,
                        json={"username": username, "password": password},
                        timeout=10.0
                    )
                    break  # If request succeeded, break the loop
                except httpx.RequestError as e:
                    if attempt < 2:  # Try again if this wasn't the last attempt
                        wait_time = 2 ** attempt  # Exponential backoff (1, 2, 4 seconds)
                        logger.warning(f"Authentication attempt {attempt+1} failed: {str(e)}. Retrying in {wait_time}s")
                        await asyncio.sleep(wait_time)
                    else:
                        # Last attempt failed
                        raise
            
            # Check response from Django backend
            if response.status_code == 200:
                # Authentication successful
                logger.info(f"Authentication successful for user: {username}")
                return cl.User(identifier=username, metadata={"provider": "django"}) 
            elif response.status_code == 401:
                # Invalid credentials
                logger.warning(f"Authentication failed for user: {username} - Invalid credentials")
                return None
            else:
                # Other backend error
                logger.error(f"Error verifying credentials. Status: {response.status_code}, Response: {response.text}")
                return None

        except httpx.RequestError as exc:
            # Connection or other request error
            logger.error(f"HTTP request error while requesting {exc.request.url!r}: {exc}")
            return None
        except Exception as e:
            # Other unexpected errors
            logger.exception("An unexpected error occurred during authentication")
            return None
    
    async def close(self):
        """Clean up resources by closing the HTTP client."""
        await self.http_client.aclose()
