"""A client for ChromaDB."""
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import streamlit as st


class ChromaDB:
    """A class for creating a client for ChromaDB."""

    def __init__(self, api_key, path="tmp/chroma"):
        """Initialize the client."""
        self.client = chromadb.PersistentClient(path=path)
        self.api_key = api_key
        self.embedding_function = OpenAIEmbeddingFunction(
            api_key=self.api_key, model_name="text-embedding-3-small"
        )
        self.client.heartbeat()

    def get_collection(self, name):
        """Get a Chroma collection."""
        try:
            collection = self.client.get_collection(
                name=name,
                embedding_function=self.embedding_function
            )
            return collection
        except AttributeError:
            return st.error("An error ocurred while getting the collection.")

    def create_collection(self, name):
        """Create a Chroma collection."""
        try:
            collection = self.client.get_or_create_collection(
                name=name,
                embedding_function=self.embedding_function
            )
            return collection
        except AttributeError:
            return st.error("An error ocurred while creating the collection.")
