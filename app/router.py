from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, Field
from typing import List
import rootutils

rootutils.setup_root(__file__, indicator=['.git', 'pyproject.toml'], pythonpath=True)

from app.vectorstore import init_vectorstore, store_text_vector, create_collection
from app.utils import embed_text, process_document, process_query

routerQ = APIRouter(tags=["Queries"])
routerI = APIRouter(tags=["Ingests"])

client = init_vectorstore()
create_collection(client)

class CitationsModel(BaseModel):
    doc: str
    page: int
    score: float
    snippet: str

class ResponseModelQuery(BaseModel):
    answer: str | None
    citations: List
    meta: dict

class ResponseModelIngest(BaseModel):
    documents_indexed: int

class QueryRequest(BaseModel):
    query_text: str = Field(..., description="Įveskite užklausą")
    k: int = Field(default=4, ge=1, le=50, description="k skaičius (1-50)")

@routerI.post('/ingest', response_model=ResponseModelIngest, status_code=201)
def ingest_documents(paths: List[str] = Body(..., description="enter paths of documents",embed=True)):
    success = 0
    for path in paths:
        try:
            for chunk in process_document(path=path):
                chunk_text_vector = embed_text(text=chunk["text"])
                store_text_vector(client,
                                  collection_name="docs",
                                  text=chunk["text"],
                                  vector=chunk_text_vector,
                                  payload={"doc": chunk['doc'], "page": chunk['page'], "text": chunk["text"]}
                                  )
            success+=1
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return ResponseModelIngest(documents_indexed = success)

@routerQ.post('/query', response_model=ResponseModelQuery, status_code=201)
def query(request: QueryRequest):
    question = request.query_text
    k = request.k

    answer, citations, meta = process_query(client=client, query=question, k=k)


    return ResponseModelQuery(
        answer= answer,
        citations=citations,
        meta=meta
    )

