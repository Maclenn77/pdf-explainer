""" A simple example of Streamlit. """
from datetime import datetime as Date
import textwrap
import os
import tiktoken
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import fitz
import streamlit as st
import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

chroma_client = chromadb.PersistentClient(path="tmp/chroma")
chroma_client.heartbeat()


def set_api_key():
    """Set the OpenAI API key."""
    openai.api_key = st.session_state.api_key
    st.write("Your API key is setup ")


openai.api_key = os.getenv("OPENAI_API_KEY")

if os.getenv("OPENAI_API_KEY") is None:
    st.warning("Add your OpenAI API key")
    openai.api_key = st.text_input(
        "Enter your OpenAI API key",
        value="",
        type="password",
        key="api_key",
        on_change=set_api_key,
        label_visibility="collapsed",
    )
    st.write("You can find your API key at https://beta.openai.com/account/api-keys")
    client = OpenAI(api_key=openai.api_key)
    embedding_function = OpenAIEmbeddingFunction(
        api_key=openai.api_key, model_name="text-embedding-ada-002"
    )
    collection = chroma_client.get_or_create_collection(
        name="pdf-explainer", embedding_function=embedding_function
    )
else:
    client = OpenAI()
    embedding_function = OpenAIEmbeddingFunction(
        api_key=openai.api_key, model_name="text-embedding-ada-002"
    )
    collection = chroma_client.get_or_create_collection(
        name="pdf-explainer", embedding_function=embedding_function
    )


# Query ChromaDb
query = st.text_input("Query ChromaDb", value="", placeholder="Enter query")
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
        text = chr(12).join([page.get_text() for page in doc])
        st.write(text[0:200])
        if st.button("Add to collection"):
            collection.add(
                documents=[text],
                metadatas=[{"source": pdf.name}],
                ids=[pdf.name + str(Date.now())],
            )
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
