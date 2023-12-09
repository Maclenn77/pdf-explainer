from src.openai_client import create_client
from src.collection_creator import create_collection


def build(chroma_client, api_key=None):
    """Build the app."""
    client = create_client(api_key=api_key)
    collection = create_collection(chroma_client, api_key=api_key)

    return client, collection
