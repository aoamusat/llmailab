# groq_vision.py
"""
This module provides functionality to interact with the Groq Vision API for image processing.

The module sets up the necessary configuration and provides utilities to work with
the Groq Vision API, particularly for encoding and sending images.

Dependencies:
    - groq: The official Groq API client library
    - base64: For encoding image data
    - os: For accessing environment variables

Configuration:
    MODEL_ID: The ID of the Groq Vision model to use (llama-3.2-90b-vision-preview)
    GROQ_API_KEY: API key retrieved from environment variables
"""

import base64
import os
import re
import requests
from groq import Groq
from langsmith import traceable

# The model identifier for the Groq Vision API
MODEL_ID = "llama-3.2-90b-vision-preview"

# Retrieve the API key from environment variables
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Define the expected output format for product descriptions
# This format specifies that responses should be JSON with two fields:
# - product_name: A text field containing the name of the product
# - description: A text field containing the product description
OUTPUT_FORMAT = """
{
  "product_name": "text",
  "description": "text"
}
"""


def encode_image(image_source):
    """
    Encodes an image to base64 format for API transmission. Accepts either a local file path
    or a URL.

    Args:
        image_source (str): The file path or URL of the image to be encoded

    Returns:
        str: Base64 encoded string representation of the image

    Raises:
        FileNotFoundError: If the specified image file does not exist
        IOError: If there are issues reading the image file
        ValueError: If the image_source is not a valid file path or URL
        requests.exceptions.RequestException: If there are issues downloading the URL
    """

    if not isinstance(image_source, str):
        raise ValueError("Image source must be a string (file path or URL)")

    # Check if input is URL using regex
    url_pattern = re.compile(
        r"^https?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain
        r"localhost|"  # localhost
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    if url_pattern.match(image_source):
        # Handle URL
        response = requests.get(image_source, timeout=30)
        response.raise_for_status()  # Raises exception for unsuccessful status codes
        return base64.b64encode(response.content).decode("utf-8")
    else:
        # Handle local file
        if not os.path.exists(image_source):
            raise FileNotFoundError(f"Image file not found: {image_source}")

        with open(image_source, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")


@traceable
def pipeline(image_source: str):
    # Initialize the Groq client with the API key
    client = Groq(api_key=GROQ_API_KEY)
    base64_image = encode_image(image_source)

    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Generates product descriptions for this item image. output should be a JSON in this format: {OUTPUT_FORMAT}",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    return completion


if __name__ == "__main__":
    # IMG_URL = "https://i.ebayimg.com/thumbs/images/g/y8QAAOSwMttkPN7Z/s-l500.jpg" # The image was used to test NSFW images
    IMG_URL = "https://i.ebayimg.com/images/g/XzoAAOSwtMVnhCyw/s-l1600.webp"
    response = pipeline(IMG_URL)
    print(f"Number of choices: {len(response.choices)}")
    print("Model: " + response.model)
    print("First model response: " + response.choices[0].message.content)
