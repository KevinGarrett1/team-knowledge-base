from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from src.embeddings import create_embeddings


def create_vector_store(
    documents: List[Document],
    embeddings=None,
):
    """
    Create a FAISS vector store from document chunks.
    """
    if embeddings is None:
        embeddings = create_embeddings()

    return FAISS.from_documents(documents, embeddings)


def save_vector_store(vectorstore: FAISS, path: str = "vector_index"):
    """
    Save FAISS vector store to disk.
    """
    vectorstore.save_local(path)


def load_vector_store(path: str = "vector_index", embeddings=None):
    """
    Load FAISS vector store from disk.
    """
    if embeddings is None:
        embeddings = create_embeddings()

    return FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True,
    )


def search(vectorstore: FAISS, query: str, k: int = 3):
    """
    Search for similar documents.
    """
    return vectorstore.similarity_search(query, k=k)


def search_with_scores(vectorstore: FAISS, query: str, k: int = 3):
    """
    Search for similar documents with scores.
    """
    return vectorstore.similarity_search_with_score(query, k=k)
