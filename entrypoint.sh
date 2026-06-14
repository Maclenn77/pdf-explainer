#!/bin/bash
python -c "from gnosis.persistence import pull; pull()"
exec streamlit run GnosisPages.py \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --server.fileWatcherType none \
    --server.port 8501
