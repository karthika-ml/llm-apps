import re
import os
from groq import Groq
import numpy as np
import requests
from langchain_core.tools import tool
from huggingface_hub import InferenceClient  # for embeddings

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_LLM_MODEL = os.getenv('GROQ_LLM_MODEL')
db = os.getenv('DB_file_name')


class VectorStoreRetriever:
    '''
    VectorStoreRetriever is a simple vector similarity search engine.
        Embeds documents into vectors.
        Stores them in memory.
        Accepts a query and returns the top-k most similar documents using cosine-like similarity (dot product).
    '''
    def __init__(self, docs: list, vectors: list):
        self._arr = np.array(vectors) # corresponding embedding as numpy
        self._docs = docs # original text

    @classmethod
    def from_docs(cls, docs):
        client = InferenceClient(model="sentence-transformers/all-MiniLM-L6-v2") # load an embedding model
        embeddings = [
            client.feature_extraction(doc["page_content"]) for doc in docs # create an embedding for the content in docs
        ]
        # return an instance of the class
        return cls(docs, embeddings)

    def query(self, query: str, k: int = 5) -> list[dict]:
        # now embed the incoming query as well
        client = InferenceClient(model="sentence-transformers/all-MiniLM-L6-v2")
        query_embed = client.feature_extraction(query)

        # caluclate similarity score by dot product of query embedding vs each document vector
        # then select topk k relevant documents and return them
        scores = np.array(query_embed) @ self._arr.T
        top_k_idx = np.argpartition(scores, -k)[-k:]
        top_k_idx_sorted = top_k_idx[np.argsort(-scores[top_k_idx])]
        return [
            {**self._docs[idx], "similarity": scores[idx]} for idx in top_k_idx_sorted
        ]

class LookupPolicyInput(BaseModel):
    query: str

@tool(args_schema=LookupPolicyInput)
def lookup_policy(query: str) -> str:
    """Consult the company policies to check whether certain options are permitted.
    Use this before making any flight changes or performing other 'write' events."""
    docs = retriever.query(query, k=2)
    return "\n\n".join([doc["page_content"] for doc in docs])

if __name__ == "__main__":
    # Get the FAQ text
    response = requests.get(
        "https://storage.googleapis.com/benchmarks-artifacts/travel-db/swiss_faq.md"
    )

    # check if http requested connects
    # status code of 200 (OK), nothing happens, and the script continues
    # request failed (e.g. 404 Not Found, 500 Internal Server Error), 
    # it raises an exception (HTTPError) and stops the program
    response.raise_for_status()
    # extracts the body content of the HTTP response as a string
    faq_text = response.text
    docs = [{"page_content": txt} for txt in re.split(r"(?=\n##)", faq_text)]
    retriever = VectorStoreRetriever.from_docs(docs)