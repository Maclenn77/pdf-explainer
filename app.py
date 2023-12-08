""" A simple example of Streamlit. """
import streamlit as st
from tika import parser

pdf = st.file_uploader("Upload a file", type="pdf")

if st.button("Extract text"):
    if pdf is not None:
        extracted_text = parser.from_file(pdf)
        st.write(extracted_text["content"])
    else:
        st.write("Please upload a file of type: pdf")
