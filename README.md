Week 13 Team Challenge – Knowledge Base Demo (Python Quality)
Overview

This repository is a working demonstration of the Week 13 Team Challenge.

It showcases how a team can build and use a retrieval-augmented knowledge base (RAG) to centralize Python quality standards across an organization.

All core infrastructure has already been implemented, tested locally, and validated through GitHub Actions. The remaining team work focuses on content, standards, and collaboration, not debugging infrastructure.

What This Demo Represents

In many real-world organizations, Python quality issues don’t come from lack of skill, but from inconsistent standards:

Different naming conventions across teams

Unclear expectations around structure and organization

Tribal knowledge instead of documented guidance

New engineers guessing instead of referencing standards

This project demonstrates how those problems can be addressed by:

Encoding Python standards as team-authored documents

Indexing them into a shared knowledge base

Making them queryable through a RAG system

Enforcing consistency through CI and review

Each document in the knowledge_base/ directory represents an agreed-upon organizational standard.

Knowledge Base Scope: Python Quality

The shared knowledge base focuses on Python quality across an organization.

The documents are organized around eight common problem areas that show up repeatedly in enterprise Python codebases.

The 8 Python Quality Areas

Naming conventions

Code organization and structure

Commenting and docstrings

Readability and simplicity

Error handling and defensive coding

Testing expectations

Dependency and environment management

Code review and consistency standards

Each team member contributes two documents, for a total of eight documents covering these areas.

Repository Structure
team-knowledge-base/
├── knowledge_base/        # Team-authored standards and guidance
├── src/                   # RAG, ingestion, retrieval infrastructure
├── tests/                 # Unit and integration tests
├── .github/workflows/     # CI validation (lint + tests)
├── TEAM.md                # Team roles and document ownership
└── README.md


For contributors:
knowledge_base/ is where you work.
The infrastructure already exists to ingest and serve your documents.

What’s Already Implemented

All of the following have already been completed and validated:

Document loading and metadata parsing

Chunking and preprocessing

Embeddings and vector store integration

Retrieval-augmented generation with source attribution

Unit and integration tests

GitHub Actions CI (lint + test)

Dependency alignment for current LangChain packages

This repository runs successfully locally and in CI.

You do not need to modify the infrastructure to participate.

How to Interact With the Knowledge Base

There’s no need to modify the infrastructure or underlying code to use this project.

All core components — loading, chunking, embeddings, vector storage, retrieval, and generation — are already implemented, tested locally, and validated through GitHub Actions.

The fastest and intended way to interact with the application is to run the provided demo script.

Quick Start (Local)

From the project root:

python demo.py


This will:

Load all documents from the knowledge_base/ directory

Chunk and process the documents

Build the vector index

Start an interactive prompt where you can ask questions

Once the system is ready, you’ll see:

Knowledge base ready. Ask a question (Ctrl+C to exit).

Example Questions

You can ask natural-language questions such as:

What are Python naming conventions?

How should Python code be organized in this organization?

What the System Returns

For each question, the system returns:

A generated answer based only on the indexed documents

A list of source documents used to produce that answer

This keeps responses grounded in documented standards, not assumptions or hallucinations.

Adding or Updating Standards

For this challenge and demo:

The Python code is already complete

CI is already configured and passing

No infrastructure changes are required

If you’re adding new standards or guidance:

Add new documents to the knowledge_base/ directory

Follow the required metadata format

Commit via a feature branch and open a PR

Re-running demo.py is enough to pick up new documents and make them queryable.

Contributor Expectations (Summary)

As a contributor (Team Member 2–4), you are expected to:

Write two structured documents

Follow the metadata header format

Submit changes via a feature branch and PR

Review at least one other contributor’s PR

CI will automatically validate that nothing breaks.

See TEAM.md for exact roles and assignments.