"""OpenAI client creator."""
import os
from openai import OpenAI


def create_client(api_key=None):
    """Create an OpenAI client."""
    if os.getenv("OPENAI_API_KEY"):
        api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    return client
