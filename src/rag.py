from typing import List, Dict, Any

from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_aws import ChatBedrock

import boto3

from src.loader import load_knowledge_base, create_chunks
from src.vectorstore import (
    create_embeddings,
    create_vector_store,
    search
)


class TeamKnowledgeBase:
    """
    Retrieval-Augmented Generation system for team knowledge.
    """

    def __init__(self, region: str = "us-east-1"):
        self.documents: List[Document] = []
        self.chunks: List[Document] = []
        self.vectorstore = None

        self.llm = ChatBedrock(
            model_id="us.amazon.nova-lite-v1:0",
            client=boto3.client("bedrock-runtime", region_name=region),
            model_kwargs={
                "temperature": 0.2,
                "max_tokens_to_sample": 800
            }
        )

        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "You are an assistant answering questions using only the provided context.\n\n"
                "Context:\n{context}\n\n"
                "Question: {question}\n\n"
                "Answer:"
            )
        )

    def load(self, directory: str = "knowledge_base") -> int:
        """Load documents from the knowledge base directory."""
        self.documents = load_knowledge_base(directory)
        return len(self.documents)

    def process(self, chunk_size: int = 500, overlap: int = 50) -> int:
        """Chunk loaded documents."""
        self.chunks = create_chunks(
            self.documents,
            chunk_size=chunk_size,
            chunk_overlap=overlap
        )
        return len(self.chunks)

    def index(self) -> int:
        """Create the vector index."""
        embeddings = create_embeddings()
        self.vectorstore = create_vector_store(self.chunks, embeddings)
        return self.vectorstore.index.ntotal

    def ask(self, question: str, k: int = 3) -> Dict[str, Any]:
        """Ask a question against the knowledge base."""
        if not self.vectorstore:
            return {
                "answer": "Knowledge base is not initialized.",
                "sources": []
            }

        results = search(self.vectorstore, question, k=k)

        if not results:
            return {
                "answer": "No relevant information found in the knowledge base.",
                "sources": []
            }

        context = "\n\n".join(doc.page_content for doc in results)

        prompt_text = self.prompt.format(
            context=context,
            question=question
        )

        response = self.llm.invoke(prompt_text)

        sources = [
            {
                "file": doc.metadata.get("source", "Unknown"),
                "author": doc.metadata.get("author", "Unknown"),
                "topic": doc.metadata.get("topic", "Unknown"),
            }
            for doc in results
        ]

        return {
            "question": question,
            "answer": response.content,
            "sources": sources
        }
