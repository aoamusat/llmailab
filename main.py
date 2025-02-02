"""
This module implements a simple chat pipeline using the Groq API and LangChain framework.

The pipeline takes user input, processes it through the Mixtral-8x7b-32768 model,
and returns the model's response.

Dependencies:
    - config: Custom module for environment variable management
    - langchain_groq: Groq integration for LangChain
    - langsmith: Tracing functionality
    - langchain_core.messages: Message types for chat models
"""

from langchain_groq import ChatGroq
from langsmith import traceable
from config import read_env_file, set_env_variables
from helpers import fetch_groq_models


# Setup environment variables from .env file
ENV_FILE = ".env"
env_vars = read_env_file(ENV_FILE)
set_env_variables(env_vars)

llm_models = fetch_groq_models()

# Initialize the Groq chat model with Mixtral-8x7b-32768
# temperature=0.8 provides a good balance between creativity and coherence
model = ChatGroq(model="llama3-70b-8192", temperature=0.8)


@traceable  # Enables automatic tracing of function execution
def pipeline(user_input: str) -> str:
    """
    Process user input through the chat model and return the response.

    Args:
        user_input (str): The input text from the user

    Returns:
        str: The model's response to the user input

    Example:
        >>> pipeline("Hello, world!")
        'Hello there! How can I assist you today?'
    """
    output = model.invoke([{"role": "user", "content": user_input}])
    return output.content


PROMPT = ""
while PROMPT == "":
    PROMPT = str(input("Enter your prompt: "))
print("Generating response. Please wait...")
response = pipeline(PROMPT)
print("Response:\n", response)
