"""Search Tool"""

class Search:
    """Search Tool"""

    def __init__(self, chroma_db):
        """Initialize the Search Tool"""
        self.chroma_db = chroma_db

    def run(self, query: str):
        """Run the Agent"""
        if not self.chroma_db.api_key:
            return "No API key set. Please add your OpenAI API key in the sidebar."

        collection = self.chroma_db.get_collection("pdf-explainer")

        # get_collection returns a Streamlit object if something went wrong
        if not hasattr(collection, "query"):
            return "Could not access the collection. Please check your API key."

        if collection.count() == 0:
            return "No documents found. Please upload a PDF first."

        results = collection.query(query_texts=[query], n_results=5)["documents"][0]
        return "\n\n---\n\n".join(results)

    def collection_name(self):
        """Return the collection name"""
        return self.chroma_db.collection.name
