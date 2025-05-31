import chainlit as cl
import os
import httpx

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
