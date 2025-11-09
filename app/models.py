from langchain_huggingface import HuggingFaceEmbeddings
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import groq
import rootutils
import torch
rootutils.setup_root(__file__, indicator=['.git', 'pyproject.toml'], pythonpath=True)
from app.config import get_settings

settings = get_settings()

def init_embedder():
    model_name = settings.embedding_model
    return HuggingFaceEmbeddings(model_name=model_name)

# deprecated cause slow on CPU
# def init_QA_pipeline():
#     model_name = settings.qa_model
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModelForCausalLM.from_pretrained(model_name)

#     if torch.cuda.is_available():
#         model = model.to("cuda")

#     QA_pipeline = pipeline(task="text-generation", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1)
#     return QA_pipeline

def init_QA_pipeline():
    client = groq.Client(api_key=settings.groq_api_key)
    return client