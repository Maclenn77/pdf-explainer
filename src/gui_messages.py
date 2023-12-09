"""Streamlit GUI messages."""
import streamlit as st


def api_message(api_key):
    """Inform if the api key is set."""
    if api_key is None:
        return st.warning("Add your OpenAI API key")

    return st.success("Your API key is setup ")


def how_to_create_api_key_message(api_key):
    """Inform how to create an api key."""
    if api_key is None:
        return st.write(
            "You can find your API key at https://beta.openai.com/account/api-keys"
        )
