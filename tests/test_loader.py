import os
import tempfile

import pytest

from src.loader import (
    parse_metadata,
    load_knowledge_base,
    create_chunks,
)


@pytest.fixture
def sample_doc_content():
    return """---
Author: Test Author
Date: 2024-01-15
Topic: Python Basics
Summary: Test document for loader.
---

Python is a high-level programming language.
It emphasizes readability and simplicity.

This document is used for testing the loader.
"""


@pytest.fixture
def temp_knowledge_base(sample_doc_content):
    """Create a temporary knowledge_base directory with one test document."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "test_doc.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(sample_doc_content)
        yield tmpdir


def test_parse_metadata_extracts_header_fields(sample_doc_content):
    metadata, content = parse_metadata(sample_doc_content)

    assert metadata["author"] == "Test Author"
    assert metadata["topic"] == "Python Basics"
    assert metadata["summary"] == "Test document for loader."
    assert "Python is a high-level programming language" in content


def test_parse_metadata_handles_missing_header():
    content = "Plain document with no metadata header."
    metadata, parsed_content = parse_metadata(content)

    assert metadata == {}
    assert parsed_content == content


def test_load_knowledge_base_loads_documents(temp_knowledge_base):
    documents = load_knowledge_base(temp_knowledge_base)

    assert len(documents) == 1
    doc = documents[0]

    assert doc.metadata["author"] == "Test Author"
    assert doc.metadata["topic"] == "Python Basics"
    assert doc.metadata["source"] == "test_doc.txt"
    assert "Python is a high-level programming language" in doc.page_content


def test_create_chunks_preserves_metadata(temp_knowledge_base):
    documents = load_knowledge_base(temp_knowledge_base)
    chunks = create_chunks(documents, chunk_size=50, chunk_overlap=10)

    assert len(chunks) >= 1

    for chunk in chunks:
        assert "source" in chunk.metadata
        assert "author" in chunk.metadata
        assert "topic" in chunk.metadata
        assert chunk.page_content.strip() != ""
