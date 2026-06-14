"""Persistence utilities for Gnosis."""
import os
from huggingface_hub import snapshot_download
from huggingface_hub.errors import HfHubHTTPError, RepositoryNotFoundError

REPO_ID = os.getenv("HF_DATASET_REPO")
LOCAL_PATH = "tmp/chroma"

def pull():
    """Download persisted ChromaDB from HF Dataset on startup."""
    if not REPO_ID:
        return
    try:
        snapshot_download(
            repo_id=REPO_ID,
            repo_type="dataset",
            local_dir=LOCAL_PATH,
            token=os.getenv("HF_DATASET_TOKEN"),
        )
    except (HfHubHTTPError, RepositoryNotFoundError):
        os.makedirs(LOCAL_PATH, exist_ok=True)
