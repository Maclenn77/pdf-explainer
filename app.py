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
from langchain.vectorstores import Chroma

load_dotenv()

if os.getenv("OPENAI_API_KEY") is None:
    st.error("Please set OPENAI_API_KEY environment variable")
    st.stop()
else:
    openai.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()
embedding_function = OpenAIEmbeddingFunction(
    api_key=openai.api_key, model_name="text-embedding-ada-002"
)
# from openai import OpenAI

chroma_client = chromadb.PersistentClient(path="tmp/chroma")
chroma_client.heartbeat()

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
            result[0:150]
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
                chunks = textwrap.wrap(text, 24000)
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

if chroma_client.get_collection(collection.name) is not None:
    langchain_agent = Chroma(client=chroma_client,
                             collection_name=collection.name,
                             embedding_function=embedding_function
                             )
     


