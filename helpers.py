"""
Groq API Client Module

This module provides functionality to interact with the Groq API,
including fetching available models and other API operations.

Required Environment Variables:
    GROQ_API_KEY: API key for authentication
    GROQ_API_URL: Base URL for the Groq API

Dependencies:
    requests: For making HTTP requests
    os: For accessing environment variables
"""

import os
import requests


def fetch_groq_models():
    """
    Fetches available models from the Groq API.

    This function retrieves the list of available models from the Groq API endpoint.
    It requires GROQ_API_KEY and GROQ_API_URL environment variables to be set.

    Returns:
        None - Prints the JSON response from the API containing model information

    Raises:
        requests.exceptions.RequestException: If the API request fails
        KeyError: If required environment variables are not set
    """
    api_key = os.environ.get("GROQ_API_KEY")
    base_url = os.environ.get("GROQ_API_URL")
    url = f"{base_url}/models"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    response = requests.get(url, headers=headers, timeout=30)
    return response.json()
