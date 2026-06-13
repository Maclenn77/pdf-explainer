"""Module for building the Langchain Agent"""
import os

import streamlit as st
from openai import AuthenticationError, APIConnectionError, BadRequestError
from langchain_openai import ChatOpenAI

from gnosis.agent import PDFExplainer

def build(key, client):
    """An Agent builder"""
    # Build Agent
    try:
        key = os.environ.get("OPENAI_API_KEY") or key
        llm = ChatOpenAI(
            temperature=st.session_state.temperature,
            model="gpt-4o-mini",
            api_key=key
            )
        agent = PDFExplainer(
            llm,
            client,
            extra_tools=st.session_state.wk_button,
        ).agent
    except AuthenticationError:
        st.warning("Invalid OpenAI API Key. Check your credentials.")
    except APIConnectionError:
        st.warning("Could not connect to OpenAI. Check your network connection.")
    except BadRequestError as e:
        st.warning(f"Bad request: {e}")
    except ValueError as e:
        st.warning(f"Configuration error: {e}")

    return agent
