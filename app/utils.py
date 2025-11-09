from typing import List
import rootutils
rootutils.setup_root(__file__, indicator=['.git', 'pyproject.toml'], pythonpath=True)

from app.models import init_embedder, init_QA_pipeline
from app.vectorstore import query_top_k
from langchain_text_splitters import CharacterTextSplitter

EMBEDDER = init_embedder()
QA_PIPELINE = init_QA_pipeline()

def embed_text(text: str) -> List[float]:
    return EMBEDDER.embed_documents([text])[0]

def split_into_chunks(text: str):
    splitter =  CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100, length_function=len)
    return splitter.split_text(text)

def process_document(path: str):
    import fitz
    doc = fitz.open(path)
    for page_num, page in enumerate(doc):
        text = page.get_text()
        for chunk in split_into_chunks(text):
            yield {
                "text": chunk,
                "doc": path,
                "page": page_num + 1
            }

def extract_context_from_answers(answers, threshold):
    context_parts = []
    citations = []
    if not isinstance(answers, list):
        answers = [answers]

    for answer in answers:
        if answer.score > threshold:
            context_parts.append(answer.payload["text"])
            citations.append({"doc": answer.payload["doc"], "page": answer.payload["page"], "score": answer.score, "snippet": answer.payload["text"]})
            

    return "\n".join(context_parts).strip(), citations

# def generate_answer(query, context):
#     if not context.strip():
#         return None
#     system_prompt = f"""
#     You are a smart assistant specializing in answering questions using the context you have.
#     Question: {query}
#     Context:
#     {context}
#     """
#     answer = QA_PIPELINE(system_prompt)
#     return answer[0]['generated_text']

def generate_answer(query, context):
    if not context.strip():
        return None
    system_prompt = f"""
    You are a smart assistant specializing in answering questions using ONLY the context you have.
    If you don't have enough context, simply answer with "Not enough information", nothing else
    """
    response = QA_PIPELINE.chat.completions.create(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Question: {query} Context: {context}"}])
    if response.choices[0].message.content == "Not enough information":
        return None
    return response.choices[0].message.content

def process_query(client, query, k, collection_name="docs", threshold=0.4):
    abstained = False
    query_text_vector = embed_text(query)
    answers = query_top_k(client=client, collection_name=collection_name, query_vector=query_text_vector, k=k)

    context, citations = extract_context_from_answers(answers=answers, threshold=threshold)

    final_answer = generate_answer(query=query, context=context)

    if final_answer:
        meta = {"retrieval_k": k, "abstained": abstained}
    else:
        abstained = True
        final_answer = None
        citations = []
        meta = {"abstained": abstained, "reason": "insufficient_evidence"}

    return final_answer, citations, meta


