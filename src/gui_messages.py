"""Streamlit GUI messages."""
import streamlit as st


def api_message(api_key):
    """Inform if the api key is set."""
    if api_key is None:
        return st.warning("Add your OpenAI API key")

    return st.success("Your API key is setup ")
