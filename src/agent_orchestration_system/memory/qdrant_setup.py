import os
import uuid
from typing import List, Dict, Any

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from litellm import embedding

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "agent_memories"
NVIDIA_EMBEDDING_MODEL = os.getenv("NVIDIA_EMBEDDING_MODEL", "nvidia_nim/nvidia/nv-embedqa-e5-v5")
# nv-embedqa-e5-v5 has 1024 dimensions
EMBEDDING_DIMENSIONS = 1024

def get_qdrant_client() -> QdrantClient:
    """Returns a Qdrant client connection."""
    return QdrantClient(url=QDRANT_URL)

def setup_qdrant_collection():
    """Initializes the Qdrant collection if it doesn't exist."""
    client = get_qdrant_client()
    
    if not client.collection_exists(collection_name=COLLECTION_NAME):
        print(f"Creating Qdrant collection: {COLLECTION_NAME}")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIMENSIONS, distance=Distance.COSINE),
        )
        print("Collection created successfully.")
    else:
        print(f"Collection {COLLECTION_NAME} already exists.")

def generate_embedding(text: str, is_query: bool = False) -> List[float]:
    """Generates a vector embedding using LiteLLM and Nvidia."""
    # nv-embedqa-e5-v5 requires input_type
    input_type = "query" if is_query else "passage"
    response = embedding(
        model=NVIDIA_EMBEDDING_MODEL,
        input=[text],
        input_type=input_type
    )
    return response['data'][0]['embedding']

def save_episodic_memory(tenant_id: str, task_id: str, objective: str, plan: str, final_result: str):
    """Saves a completed task's details into Qdrant as an episodic memory."""
    client = get_qdrant_client()
    
    # We embed the objective to find it later
    vector = generate_embedding(objective)
    
    payload = {
        "tenant_id": tenant_id,
        "task_id": task_id,
        "objective": objective,
        "plan": plan,
        "final_result": final_result
    }
    
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload=payload
            )
        ]
    )

def search_similar_tasks(tenant_id: str, current_objective: str, limit: int = 3) -> List[Dict[str, Any]]:
    """Searches Qdrant for similar past tasks for the same tenant."""
    client = get_qdrant_client()
    vector = generate_embedding(current_objective, is_query=True)
    
    search_result = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="tenant_id",
                    match=MatchValue(value=tenant_id)
                )
            ]
        ),
        limit=limit
    )
    
    return [hit.payload for hit in search_result.points]

if __name__ == "__main__":
    setup_qdrant_collection()
