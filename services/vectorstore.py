import httpx

from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_core.documents import Document
from langchain_redis import RedisVectorStore
from datetime import datetime

from core.settings import OLLAMA_HOST


class OllamaEmbedding(Embeddings):
    def __init__(self, model_name="nomic-embed-text"):
        self.model_name = model_name

    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            try:
                response = httpx.post(
                    f"{OLLAMA_HOST}/api/embeddings",
                    json={"model": self.model_name, "prompt": text},
                    timeout=30.0,
                )
                embedding = response.json().get("embedding")
                embeddings.append(embedding)
            except Exception:
                embeddings.append([0.0] * 768)
        return embeddings

    def embed_query(self, text):
        return self.embed_documents([text])[0]


def create_vector_store(config) -> VectorStore:
    return RedisVectorStore(
        embeddings=OllamaEmbedding(), config=config, ttl=60 * 60
    )  # 1 hour TTL


def save_doc(vector_store: VectorStore, question: str, answer: str):
    doc = Document(
        page_content=question,
        metadata={
            "response": answer,
            "question": question,
            "created_at": datetime.now().isoformat(),
        },
    )
    vector_store.add_documents([doc])


def get_similar_answer(
    vector_store, query: str, show_options=False, similarity_threshold=0.85
):
    results = vector_store.similarity_search_with_score(query, k=3)
    most_similar = None
    highest_similarity = 0.0

    for doc, score in results:
        similarity = 1 - score
        response = doc.metadata.get("response")
        question = doc.metadata.get("question")

        if show_options:
            print(f"Option: {question} (similarity: {similarity:.2f})")

        if similarity >= similarity_threshold and similarity > highest_similarity:
            highest_similarity = similarity
            most_similar = response

    return most_similar