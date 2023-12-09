"""Create a Chroma collection."""
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import streamlit as st


def create_collection(client, name="pdf-explainer", api_key=None):
    """Create a Chroma collection."""
    try:
        embedding_function = OpenAIEmbeddingFunction(
            api_key=api_key, model_name="text-embedding-ada-002"
        )
        collection = client.get_or_create_collection(
            name=name, embedding_function=embedding_function
        )
        return collection
    except AttributeError as e:
        st.error("An error ocurred while creating the collection." + e.with_traceback)
