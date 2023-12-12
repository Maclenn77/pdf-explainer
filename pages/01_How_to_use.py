"""Instructions on how to use the website"""
import streamlit as st

# Title of the page
st.title("How to use this website")
st.markdown(
    "1. **Add your OpenAI API key**: You can get it from [here](https://beta.openai.com/).",
    unsafe_allow_html=True,
)
st.image(image="pages/images/01_Add_API_Key.png", caption="Add your OpenAI API key")
st.markdown(
    "2. **Upload a PDF file**: It should be a PDF file with text. Scanned pages are not supported."
)
st.image(image="pages/images/02_Upload_PDF.png", caption="Upload a PDF file")
st.markdown(
    "3. **Save chunks**: Text is extracted, splitted and save in chunks on ChromaDB."
)
st.image(image="pages/images/03_Save_Chunks.png", caption="Save chunks")
st.markdown(
    "4. **Consult your knowledge base**: You can consult your knowledge base with the chatbot."
)
st.image(image="pages/images/04_Consult_KB.png", caption="Consult your knowledge base")
st.markdown(
    "5. **Use Wikipedia**: You can use Wikipedia to enrich your knowledge base."
)
st.image(image="pages/images/05_Use_Wikipedia.png", caption="Use Wikipedia")
st.markdown(
    '6. **Change creativity level**: Also called "temperature". As higher, more unexpected results.'
)
st.image(image="pages/images/06_Creativity.png", caption="Change creativity level")
st.markdown("7. **Delete collection**: You can delete your collection and start over.")
st.image(image="pages/images/07_Delete_Collection.png", caption="Delete collection")
st.write("That's all! Enjoy!")
