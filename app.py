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


def click_wk_button():
    """Set the OpenAI API key."""
    st.session_state.wk_button = not st.session_state.wk_button


openai.api_key = os.getenv("OPENAI_API_KEY")

if "api_message" not in st.session_state:
    st.session_state.api_message = gm.api_message(openai.api_key)


# Build settings
chroma_db = ChromaDB(openai.api_key)
openai_client, collection = settings.build(chroma_db)

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
    if "wk_button" not in st.session_state:
        st.session_state.wk_button = False

    st.checkbox(
        "Use Wikipedia", on_change=click_wk_button, value=st.session_state.wk_button
    )
    st.subheader("Creativity")
    st.write("The higher the value, the crazier the text.")
    st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.9,
        step=0.01,
        key="temperature",
    )

    if st.button("Delete collection"):
        st.warning("Are you sure?")
        if st.button("Yes"):
            try:
                chroma_db.delete_collection(collection.name)
            except AttributeError:
                st.error("Collection erased.")

# Main
st.title("GnosisPages")
st.subheader("Create your knowledge base")

## Uploader
container = st.container()
container.write(
    "Upload, extract and consult the content of PDF Files for builiding your knowledge base!"
)
pdf = container.file_uploader("Upload a file", type="pdf")

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
    container.write("Please upload a file of type: pdf")

st.subheader("Consult your knowledge base")

chatbox = st.container()

prompt = chatbox.chat_input()

if prompt:
    # Create Agent
    try:
        openai_api_key = openai.api_key
        llm = ChatOpenAI(
            temperature=st.session_state.temperature,
            model="gpt-3.5-turbo-16k",
            api_key=openai.api_key,
        )
        agent = PDFExplainer(
            llm,
            chroma_db,
            extra_tools=st.session_state.wk_button,
        ).agent
    except Exception:  # pylint: disable=broad-exception-caught
        st.warning("Missing OpenAI API Key.")

    chatbox.chat_message("user").write(prompt)
    with chatbox.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(prompt, callbacks=[st_callback])
        chatbox.write(response)
