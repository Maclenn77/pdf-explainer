"""Search Tool"""


class Search:
    """Search Tool"""

    def __init__(self, chroma_db):
        """Initialize the Search Tool"""
        self.chroma_db = chroma_db

    def run(self, query: str):
        """Run the Agent"""
        collection = self.chroma_db.get_collection("pdf-explainer")
        return collection.query(query_texts=[query], n_results=3)["documents"][0]

    def collection_name(self):
        """Return the collection name"""
        return self.chroma_db.collection.name
