""" A simple example of Streamlit. """
import streamlit as st
import fitz

# from tika import parser
# from openai import OpenAI

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

pdf = st.file_uploader("Upload a file", type="pdf")

if st.button("Extract text"):
    if pdf is not None:
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc:  # open document
            text = chr(12).join([page.get_text() for page in doc])
            st.write(text)
    else:
        st.write("Please upload a file of type: pdf")
