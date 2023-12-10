"""Build settings for the app."""


def build(chroma_db):
    """Build the app."""
    collection = chroma_db.create_collection("pdf-explainer")

    return collection
