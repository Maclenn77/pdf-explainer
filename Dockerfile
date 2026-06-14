FROM python:3.11.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY wk_flow_requirements.txt .
RUN pip install --no-cache-dir -r wk_flow_requirements.txt

COPY GnosisPages.py .
COPY gnosis/ ./gnosis/
COPY pages/ ./pages/

RUN mkdir -p /app/tmp/chroma

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "GnosisPages.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--server.enableCORS=false", \
    "--server.enableXsrfProtection=false", \
    "--server.fileWatcherType=none"]
    
