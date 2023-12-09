"""Build settings for the app."""
from src.openai_client import create_client


def build(chroma_db):
    """Build the app."""
    openai_client = create_client(chroma_db.api_key)
    collection = chroma_db.create_collection("pdf-explainer")

    return openai_client, collection
