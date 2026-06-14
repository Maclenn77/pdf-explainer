FROM python:3.11.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY wk_flow_requirements.txt .
RUN pip install --no-cache-dir -r wk_flow_requirements.txt

# Copy project files
COPY GnosisPages.py .
COPY gnosis/ ./gnosis/
COPY pages/ ./pages/

# Create tmp directory for ChromaDB
RUN mkdir -p /app/tmp/chroma

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "GnosisPages.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--server.enableCORS=false", \
    "--server.enableXsrfProtection=false"]
