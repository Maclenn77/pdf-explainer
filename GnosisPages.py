# pylint: disable=invalid-name
""" A Streamlit app for GnosisPages. """
import os
from pathlib import Path

import openai
import streamlit as st
from dotenv import load_dotenv

from gnosis.chroma_client import ChromaDB
import gnosis.gui_messages as gm
from gnosis import settings
from gnosis.components.sidebar import sidebar
from gnosis.components.main import main

load_dotenv(Path(__file__).parent / ".env")

openai.api_key = os.getenv("OPENAI_API_KEY")

if "api_message" not in st.session_state:
    st.session_state.api_message = gm.api_message(openai.api_key)


if "wk_button" not in st.session_state:
    st.session_state.wk_button = False

if "chroma_db" not in st.session_state:
    st.session_state.chroma_db = ChromaDB(openai.api_key)

# Build settings
chroma_db = st.session_state.chroma_db
collection = settings.build(chroma_db)

# Sidebar
sidebar(chroma_db, collection)

main(openai.api_key, chroma_db, collection)
