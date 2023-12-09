"""A client for ChromaDB."""
import chromadb


class ChromaDB:
    """A class for creating a client for ChromaDB."""

    def __init__(self, path="tmp/chroma"):
        """Initialize the client."""
        self.client = chromadb.PersistentClient(path=path)
        self.client.heartbeat()
