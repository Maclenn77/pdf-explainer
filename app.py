""" A simple example of Streamlit. """
import textwrap
import os
import tiktoken
import fitz
import streamlit as st
import openai
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import StreamlitCallbackHandler
from src.chroma_client import ChromaDB
import src.gui_messages as gm
from src import settings

from src.agent import PDFExplainer


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
chroma_db = ChromaDB(openai.api_key)
openai_client, collection = settings.build(chroma_db)

# Create Agent
llm = ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo-16k", api_key=openai.api_key)
agent = PDFExplainer(llm, chroma_db).agent

# Main
st.title("PDF Explainer")
st.subheader("Create your knowledge base")
st.write("Upload PDF files that will help the AI Agent to understand your domain.")
pdf = st.file_uploader("Upload a file", type="pdf")

if pdf is not None:
    with fitz.open(stream=pdf.read(), filetype="pdf") as doc:  # open document
        with st.spinner("Extracting text..."):
            text = chr(12).join([page.get_text() for page in doc])
        st.subheader("Text preview")
        st.write(text[0:300] + "...")
        if st.button("Save chunks"):
            with st.spinner("Saving chunks..."):
                chunks = textwrap.wrap(text, 1250)
                for idx, chunk in enumerate(chunks):
                    encoding = tiktoken.get_encoding("cl100k_base")
                    num_tokens = len(encoding.encode(chunk))
                    collection.add(
                        documents=[chunk],
                        metadatas=[{"source": pdf.name, "num_tokens": num_tokens}],
                        ids=[pdf.name + str(idx)],
                    )
else:
    st.write("Please upload a file of type: pdf")

st.subheader("Search on your knowledge base")
# if st.button("Chroma data collection"):
#     st.write(collection)

# if st.button("Delete Chroma Collection"):
#     try:
#         chroma_db.client.delete_collection(collection.name)
#     except AttributeError:
#         st.error("Collection erased.")

prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(prompt, callbacks=[st_callback])
        st.write(response)
