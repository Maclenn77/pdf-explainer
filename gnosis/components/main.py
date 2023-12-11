"""Main component"""
import textwrap
import tiktoken
import fitz
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
import gnosis.gui_messages as gm
from gnosis.builder import build


def uploader(collection):
    """Component for upload files"""
    st.write(
        "Upload, extract and consult the content of PDF Files for builiding your knowledge base!"
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


def main(key, client, collection):
    """Main component"""
    gm.header()

    uploader(collection)

    st.subheader("Consult your knowledge base")

    prompt = st.chat_input()

    if prompt:
        agent = build(key, client)

        st.chat_message("user").write(prompt)
        with st.chat_message("assistant"):
            st_callback = StreamlitCallbackHandler(st.container())
            response = agent.run(prompt, callbacks=[st_callback])
            st.write(response)
