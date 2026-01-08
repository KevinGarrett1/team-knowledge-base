from unittest.mock import Mock, patch

from langchain_core.documents import Document

from src.vectorstore import (
    create_vector_store,
    search,
    search_with_scores,
)


def test_create_vector_store_uses_faiss():
    docs = [
        Document(page_content="Test content", metadata={"source": "test.txt"})
    ]

    mock_embeddings = Mock()

    with patch("src.vectorstore.FAISS.from_documents") as mock_from_docs:
        mock_vectorstore = Mock()
        mock_from_docs.return_value = mock_vectorstore

        result = create_vector_store(docs, embeddings=mock_embeddings)

        mock_from_docs.assert_called_once_with(docs, mock_embeddings)
        assert result == mock_vectorstore


def test_search_calls_similarity_search():
    mock_vectorstore = Mock()
    mock_doc = Document(page_content="Result", metadata={})
    mock_vectorstore.similarity_search.return_value = [mock_doc]

    results = search(mock_vectorstore, "test query", k=1)

    mock_vectorstore.similarity_search.assert_called_once_with("test query", k=1)
    assert results == [mock_doc]


def test_search_with_scores_calls_similarity_search_with_score():
    mock_vectorstore = Mock()
    mock_doc = Document(page_content="Result", metadata={})
    mock_vectorstore.similarity_search_with_score.return_value = [(mock_doc, 0.42)]

    results = search_with_scores(mock_vectorstore, "test query", k=1)

    mock_vectorstore.similarity_search_with_score.assert_called_once_with(
        "test query", k=1
    )
    assert results[0][1] == 0.42
