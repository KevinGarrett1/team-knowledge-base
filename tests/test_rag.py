from unittest.mock import patch, Mock

from src.rag import TeamKnowledgeBase


def test_ask_without_index():
    with patch("src.rag.ChatBedrock"):
        kb = TeamKnowledgeBase()
        result = kb.ask("What is Python?")
        assert "not initialized" in result["answer"]
        assert result["sources"] == []


def test_ask_with_no_results():
    with patch("src.rag.ChatBedrock"):
        kb = TeamKnowledgeBase()
        kb.vectorstore = Mock()
        kb.vectorstore.similarity_search.return_value = []

        result = kb.ask("Nonexistent topic")
        assert "No relevant information" in result["answer"]
        assert result["sources"] == []


def test_sources_are_returned():
    with patch("src.rag.ChatBedrock") as mock_llm:
        mock_llm.return_value.invoke.return_value.content = "Test answer"

        kb = TeamKnowledgeBase()
        kb.vectorstore = Mock()

        mock_doc = Mock()
        mock_doc.page_content = "Test content"
        mock_doc.metadata = {
            "source": "doc.txt",
            "author": "Tester",
            "topic": "Testing"
        }

        kb.vectorstore.similarity_search.return_value = [mock_doc]

        result = kb.ask("Test question")

        assert result["answer"] == "Test answer"
        assert len(result["sources"]) == 1
        assert result["sources"][0]["file"] == "doc.txt"
