import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "agent_memories"

def get_qdrant_client() -> QdrantClient:
    """Returns a Qdrant client connection."""
    return QdrantClient(url=QDRANT_URL)

def setup_qdrant_collection():
    """Initializes the Qdrant collection if it doesn't exist."""
    client = get_qdrant_client()
    
    # Check if collection exists
    if not client.collection_exists(collection_name=COLLECTION_NAME):
        print(f"Creating Qdrant collection: {COLLECTION_NAME}")
        # We use 1536 dimensions (matching OpenAI's text-embedding-3-small)
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )
        print("Collection created successfully.")
    else:
        print(f"Collection {COLLECTION_NAME} already exists.")

if __name__ == "__main__":
    setup_qdrant_collection()
