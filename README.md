---
title: GnosisPages
emoji: 📝
colorFrom: red
colorTo: pink
sdk: streamlit
app_file: GnosisPages.py
pinned: false
license: mit
---

# GnosisPages
GnosisPages is a tool that helps you to create your own knowledge base for retrieval information when interacting with a LLM. The app take advantage of the frameworks Streamlit and Langchain and uses a client-side ChromaDB.

## Features

GnosisPages offers you the following key features:

- **Upload PDF files**: Upload PDF files until 200MB size. PDF files should be programmatically created or processed by an OCR tool.
- **Extract and split text**: Extract the content of your PDF files and split them for a better querying.
- **Store in a client-side VectorDB**: GnosisPages uses ChromaDB for storing the content of your pdf files on vectors (ChromaDB use by default "all-MiniLM-L6-v2" for embeddings)
- **Consult the info of your knowledge base**: Ask questions to the Intelligent Assitant about the content of your knowledge base. The Langchain Agent will use ChromaDB query functions as a tool.

## Demo 

[Try the GnosisPages's demo](https://huggingface.co/spaces/maclenn77/pdf-explainer)!!!

[Watch a demo here](https://youtu.be/OEQTusJGHFQ)

## Prerrequisites

For using the demo, you only need an OpenAI API Key.

If you prefer to clone the project and run on local environment, you will require:

- Python ( developed with v3.11)
- OpenAI API Key
- Langchain
- ChromaDB
- Streamlit
- A code editor

## Setup

Follow the next steps to set up GnosisPages in your local environment:

1. Clone this repository

```bash
    git clone https://github.com/maclenn77/pdf-explainer.git
```

3. Navigate to the project directory
```bash
   cd pdf-explainer
```
4. Create your .env file
```bash
   touch .env
   nano .env # or your prefered text editor
```
 And add your OpenAI API Key.
```yaml
   OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```
5. Install dependencies.
```bash
   pip install -r requirements.txt
```
6. Run on your local environment
```bash
   streamlit run GnosisPages.py
```

## Deployment

GnosisPages's repo includes workflows for deploying to HuggingFace. 

1. **Check file size**: Prevents to merge and deploy files over the limit provided by HuggingFace 🤗.
2. **Check lints**: Analize the code with pylint.
3. **Deploy to HuggingFace**: Once a branch is merged into main, the last version is deployed on a HuggingFace Space.

For deploying, you need to add `HF_TOKEN` as secret in the settings of your fork and add a HuggingFace user with the variable name `HF_USERNAME`.

## Feedback and Contributions
If you have any feedback or would like to contribute to GnosisPages's development, please feel free to open issues or submit pull requests in the GitHub repository.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

Enjoy using GnosisPages to create and consult your knowled base! If you have any questions or encounter issues during the setup process, please don't hesitate to reach out for assistance.
