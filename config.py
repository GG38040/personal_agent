"""Configuration module for managing environment variables and API keys."""

import os
from typing import Optional
from dotenv import load_dotenv

def load_config() -> None:
    """Load environment variables from .env file."""
    load_dotenv()

def get_api_key() -> str:
    """
    Retrieve the OpenAI API key from environment variables.
    
    Returns:
        str: The API key value
        
    Raises:
        ValueError: If the API key is not set in environment variables
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set. "
            "Please check your .env file."
        )
    return api_key

# Load environment variables on module import
load_config()

# Export the API key for use in other modules
OPENAI_API_KEY = get_api_key()
