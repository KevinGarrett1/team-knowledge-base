from pathlib import Path
from typing import Tuple, List

from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def parse_metadata(content: str) -> Tuple[dict, str]:
    """
    Parse a metadata header from a document.

    Expected format:
    ---
    Author: Name
    Date: YYYY-MM-DD
    Topic: Something
    Summary: Short text
    ---

    Returns:
        metadata (dict), remaining_content (str)
    """
    metadata = {}

    if not content.startswith("---"):
        return metadata, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return metadata, content

    header = parts[1].strip()
    body = parts[2].strip()

    for line in header.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip().lower()] = value.strip()

    return metadata, body


def load_knowledge_base(directory: str = "knowledge_base") -> List[Document]:
    """
    Load all .txt documents from the knowledge base directory,
    parse metadata headers, and return LangChain Document objects.
    """
    documents: List[Document] = []
    base_path = Path(directory)

    if not base_path.exists():
        raise FileNotFoundError(f"Knowledge base directory not found: {directory}")

    for file_path in base_path.glob("*.txt"):
        loader = TextLoader(str(file_path))
        loaded_docs = loader.load()

        for doc in loaded_docs:
            metadata, content = parse_metadata(doc.page_content)

            # Always attach source info
            metadata["source"] = file_path.name
            metadata["filepath"] = str(file_path)

            documents.append(
                Document(
                    page_content=content,
                    metadata=metadata,
                )
            )

    return documents


def create_chunks(
    documents: List[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> List[Document]:
    """
    Split documents into chunks while preserving metadata.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = splitter.split_documents(documents)
    return chunks
