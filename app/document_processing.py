from typing import List
from qdrant_client import QdrantClient

import rootutils
rootutils.setup_root(__file__, indicator=['.git', 'pyproject.toml'], pythonpath=True)

def create_collection(client, collection_name = "docs", size: int = 384, distance: str = "Cosine"):
    client.recreate_collection(
    collection_name=collection_name,
    vectors_config={"size": size, "distance": distance},
    )

def embed_text(embedder, text: str) -> List[List[float]]:
    return embedder.embed_documents([text])[0]

def init_vectorstore():
    return QdrantClient(host="localhost", port=6333)

def process_documents(paths: List[str]) -> int:
    success = 0
    for path in paths:
        try:
            process_document(path)
            success+=1
        except:
            continue
    return success

def split_text(text):
    pass

def store_text_vector(text: str, vector: List[float],)

def process_document(path):