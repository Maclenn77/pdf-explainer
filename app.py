""" A simple example of Streamlit. """
from datetime import datetime as Date
import chromadb
import fitz
import streamlit as st

# from openai import OpenAI

chroma_client = chromadb.PersistentClient(path="tmp/chroma")
chroma_client.heartbeat()

collection = chroma_client.get_or_create_collection("pdf-explainer")

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
        )


pdf = st.file_uploader("Upload a file", type="pdf")


if st.button("Save"):
    if pdf is not None:
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc:  # open document
            text = chr(12).join([page.get_text() for page in doc])
            st.write(text[0:200])
            collection.add(
                documents=[text],
                metadatas=[{"source": pdf.name}],
                ids=[pdf.name + str(Date.now())],
            )
    else:
        st.write("Please upload a file of type: pdf")


if st.button("Chroma data collection"):
    st.write(collection)

if st.button("Delete Chroma Collection"):
    chroma_client.delete_collection(collection.name)
    st.write("Deleted Chroma Collection")
