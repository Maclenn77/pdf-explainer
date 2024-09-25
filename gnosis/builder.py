"""Module for building the Langchain Agent"""
import streamlit as st
from langchain_openai import ChatOpenAI
from gnosis.agent import PDFExplainer


def build(key, client):
    """An Agent builder"""
    # Build Agent
    try:
        llm = ChatOpenAI(
            temperature=st.session_state.temperature,
            model="gpt-4o-mini",
            api_key=key,
        )
        agent = PDFExplainer(
            llm,
            client,
            extra_tools=st.session_state.wk_button,
        ).agent
    except Exception:  # pylint: disable=broad-exception-caught
        st.warning("Missing OpenAI API Key.")

    return agent
