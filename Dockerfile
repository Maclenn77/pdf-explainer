FROM python:3.11.9-slim

WORKDIR /app

COPY ./wk_flow_requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Create non-root user (required by HF)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user
ENV PATH=$HOME/.local/bin:$PATH

WORKDIR $HOME
RUN mkdir app
WORKDIR $HOME/app

COPY . $HOME/app

RUN mkdir -p $HOME/app/tmp/chroma

EXPOSE 8501

CMD streamlit run GnosisPages.py \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --server.fileWatcherType none \
    --server.port 8501
