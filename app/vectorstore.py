from qdrant_client import QdrantClient
from typing import List
import uuid

import rootutils
rootutils.setup_root(__file__, indicator=['.git', 'pyproject.toml'], pythonpath=True)

def init_vectorstore(host="localhost", port=6333):
    client = QdrantClient(host=host, port=port)
    return client

def create_collection(client, collection_name="docs", size: int = 384, distance: str = "Cosine"):
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config={"size": size, "distance": distance, "on_disk": True},
        )
    else:
        print(f"Collection: {collection_name}, already exists")

def store_text_vector(client, collection_name: str, text: str, vector: List[float], payload: dict):
    client.upsert(
        collection_name=collection_name,
        points=[{
            "id": str(uuid.uuid5(uuid.NAMESPACE_URL, text)),
            "vector": vector,
            "payload": payload
        }]
    )

def query_top_k(client, collection_name: str, query_vector: List[float], k: int = 4):
    return client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=k
    )
