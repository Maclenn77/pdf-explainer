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
        self._embedding_function = None  # ← lazy, not created yet
        self.client.heartbeat()

    @property
    def embedding_function(self):
        """Create embedding function only when API key is available."""
        if not self.api_key:
            return None
        if self._embedding_function is None:
            self._embedding_function = OpenAIEmbeddingFunction(
                api_key=self.api_key, model_name="text-embedding-3-small"
            )
        return self._embedding_function

    def set_api_key(self, api_key):
        """Update the API key and reset the embedding function."""
        self.api_key = api_key
        self._embedding_function = None  # force recreation with new key

    def get_collection(self, name):
        """Get a Chroma collection."""
        if not self.embedding_function:
            return st.error("Add your OpenAI API key first.")
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
        if not self.embedding_function:
            return st.error("Add your OpenAI API key first.")
        try:
            collection = self.client.get_or_create_collection(
                name=name,
                embedding_function=self.embedding_function
            )
            return collection
        except AttributeError:
            return st.error("An error ocurred while creating the collection.")
