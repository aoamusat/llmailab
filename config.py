"""
Environment variable configuration module for LangSmith and OpenAI integration.

This module handles setting up required environment variables for LangSmith tracing
and OpenAI API access, prompting for user input if variables are not already set.
"""

import os
from typing import Dict


def read_env_file(file_path):
    """
    Read environment variables from a specified file.

    Args:
        file_path (str): The path to the environment variable file.

    Returns:
        dict: A dictionary containing the environment variables read from the file.
    """
    environment_vars = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                environment_vars[key] = value
    return environment_vars


def set_env_variables(values: Dict[str, str]):
    """
    Set environment variables if they are not already set.

    Args:
        values (dict): A dictionary containing the environment variables to set.
    """

    for key, value in values.items():
        if key not in os.environ:
            os.environ[key] = value
