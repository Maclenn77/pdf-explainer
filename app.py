""" A simple example of Streamlit. """
from datetime import datetime as Date
import textwrap
import os
import tiktoken
import fitz
import streamlit as st
import openai
from dotenv import load_dotenv
from src.chroma_client import ChromaDB
import src.gui_messages as gm
import src.settings as settings

load_dotenv()


def set_api_key():
    """Set the OpenAI API key."""
    openai.api_key = st.session_state.api_key
    st.session_state.api_message = gm.api_message(openai.api_key)


openai.api_key = os.getenv("OPENAI_API_KEY")

if "api_message" not in st.session_state:
    st.session_state.api_message = gm.api_message(openai.api_key)

# Sidebar
with st.sidebar:
    st.write("## OpenAI API key")
    openai.api_key = st.text_input(
        "Enter OpenAI API key",
        value="",
        type="password",
        key="api_key",
        placeholder="Enter your OpenAI API key",
        on_change=set_api_key,
        label_visibility="collapsed",
    )
    st.write(
        "You can find your API key at https://platform.openai.com/account/api-keys"
    )

# Build settings
chroma_client = ChromaDB().client
client, collection = settings.build(chroma_client, api_key=openai.api_key)

# Query ChromaDb
query = st.text_input(
    "Query ChromaDb", value="", placeholder="Enter query", label_visibility="collapsed"
)
if st.button("Search"):
    results = collection.query(
        query_texts=[query],
        n_results=3,
    )

    for idx, result in enumerate(results["documents"][0]):
        st.markdown(
            result
            + "..."
            + "**Source:** "
            + results["metadatas"][0][idx]["source"]
            + " **Tokens:** "
            + str(results["metadatas"][0][idx]["num_tokens"])
        )


pdf = st.file_uploader("Upload a file", type="pdf")

if pdf is not None:
    with fitz.open(stream=pdf.read(), filetype="pdf") as doc:  # open document
        with st.spinner("Extracting text..."):
            text = chr(12).join([page.get_text() for page in doc])
        st.subheader("Text preview")
        st.write(text[0:300] + "...")
        if st.button("Save chunks"):
            with st.spinner("Saving chunks..."):
                chunks = textwrap.wrap(text, 3000)
                for idx, chunk in enumerate(chunks):
                    encoding = tiktoken.get_encoding("cl100k_base")
                    num_tokens = len(encoding.encode(chunk))
                    response = (
                        client.embeddings.create(
                            input=chunk, model="text-embedding-ada-002"
                        )
                        .data[0]
                        .embedding
                    )
                    collection.add(
                        embeddings=[response],
                        documents=[chunk],
                        metadatas=[{"source": pdf.name, "num_tokens": num_tokens}],
                        ids=[pdf.name + str(idx)],
                    )
else:
    st.write("Please upload a file of type: pdf")

if st.button("Chroma data collection"):
    st.write(collection)

if st.button("Delete Chroma Collection"):
    try:
        chroma_client.delete_collection(collection.name)
    except AttributeError:
        st.error("Collection erased.")
