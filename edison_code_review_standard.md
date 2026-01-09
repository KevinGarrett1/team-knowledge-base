# Project Documentation: Code Review & Consistency Standards
## 2. Code Review and Consistency Standards

### 2.1 Coding Standards

#### 2.1.1 Python Style Guide
- Follow **PEP 8** for all Python code
- Use **Black** for automatic code formatting
- Use **isort** for consistent import ordering
- Maximum line length: **88 characters**
- Use **type hints** for all function signatures
- Document all public functions with **docstrings** (Google style)

**Example:**
```python
from typing import Dict, List, Optional
from langchain.chains.llm import LLMChain


def build_simple_chain(llm: Any) -> SimpleSequentialChain:
    """Build a two-step idea generation and evaluation chain.

    Args:
        llm: The language model to use for the chain

    Returns:
        SimpleSequentialChain: Configured chain for idea generation and evaluation

    Example:
        >>> chain = build_simple_chain(llm)
        >>> result = chain.run("AI applications")
    """
    # Implementation here
```

#### 2.1.2 File Organization
- **One class/function per file** principle for larger components
- **Module-level docstrings** explaining purpose
- **Import order**: Standard library → Third-party → Local modules
- **Absolute imports** for local modules

**Example imports:**
```python
# Standard library
import os
from typing import Dict, List
from datetime import datetime

# Third-party
from langchain.chains.sequential import SimpleSequentialChain
from langchain.prompts import PromptTemplate

# Local modules
from src.client import create_client, create_llm
from src.prompts import SYSTEM_PROMPT
```

### 2.2 Testing Standards

#### 2.2.1 Test Structure
- **Test file naming**: `test_<module>.py`
- **Test function naming**: `test_<functionality>_<expected_behavior>`
- **Test class naming**: `Test<Component>`
- **Arrange-Act-Assert** pattern for all tests
- **Mock external dependencies** (AWS, APIs)

**Example test:**
```python
import pytest
from unittest.mock import Mock, patch
from src.tools import calculator


class TestCalculatorTool:
    """Test suite for calculator tool."""

    def test_calculator_addition_returns_correct_result(self):
        """Test that calculator correctly adds numbers."""
        # Arrange
        expression = "2 + 3"

        # Act
        result = calculator(expression)

        # Assert
        assert "5" in result
        assert "Result:" in result

    def test_calculator_invalid_input_returns_error(self):
        """Test that calculator rejects non-math input."""
        # Arrange
        expression = "import os"

        # Act
        result = calculator(expression)

        # Assert
        assert "Error" in result
```

#### 2.2.2 Test Coverage Requirements
- **Minimum 80%** overall coverage
- **100% coverage** for core business logic
- **Unit tests** for all public functions
- **Integration tests** for chain workflows
- **Mock AWS credentials** for CI/CD

**pytest.ini:**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80
```

### 2.3 Git and Version Control Standards

#### 2.3.1 Branch Strategy
- **main**: Production-ready code only
- **develop**: Integration branch for features
- **feature/**: New features (feature/chain-implementation)
- **bugfix/**: Bug fixes (bugfix/memory-leak)
- **release/**: Release preparation (release/v1.2.0)

#### 2.3.2 Commit Message Convention
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code restructuring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(chains): add sequential chain implementation

- Implement SimpleSequentialChain for idea generation
- Add research pipeline with three-step chain
- Update requirements.txt with langchain-core

Closes #123
```

```
fix(memory): resolve session memory leak

- Clear memory store on session deletion
- Add session cleanup function
- Update memory tests to verify cleanup

Fixes #456
```

#### 2.3.3 Pull Request Guidelines
1. **Single responsibility**: One feature/fix per PR
2. **Descriptive title**: Clear summary of changes
3. **Linked issues**: Reference issue numbers
4. **Review checklist**:
   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] Code follows standards
   - [ ] All checks pass
5. **Squash commits**: Before merging

### 2.4 CI/CD Pipeline Standards

#### 2.4.1 GitHub Actions Workflows

**.github/workflows/test.yml:**
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11"]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Run tests
      env:
        AWS_ACCESS_KEY_ID: test
        AWS_SECRET_ACCESS_KEY: test
      run: |
        pytest tests/ -v --cov=src --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

**.github/workflows/lint.yml:**
```yaml
name: Lint
on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"

    - name: Install dependencies
      run: |
        pip install black flake8 isort mypy

    - name: Check formatting with Black
      run: black --check src/ tests/

    - name: Check imports with isort
      run: isort --check-only src/ tests/

    - name: Lint with flake8
      run: flake8 src/ tests/ --max-line-length=88

    - name: Type check with mypy
      run: mypy src/
```

#### 2.4.2 Quality Gates
- **All tests must pass** before merge
- **No linting errors** allowed
- **Code coverage** minimum 80%
- **Type checking** must pass
- **Dependency security** scans clean

### 2.5 Documentation Standards

#### 2.5.1 README.md Template
```markdown
# LangChain Assistant

## Overview
Brief description of the project and its purpose.

## Features
- Feature 1: Multi-step reasoning with chains
- Feature 2: Conversation memory
- Feature 3: Custom tools (calculator, time, word counter)

## Installation
    ```bash
    git clone <repo-url>
    cd langchain-assistant
    pip install -r requirements.txt
    ```

## Usage
    ```python
    from src.chains import generate_and_evaluate
    result = generate_and_evaluate("AI applications")
    ```

## Project Structure
Explain the directory structure and key files.

## Development
Instructions for setting up development environment.

## Testing
    ```bash
    pytest tests/ -v
    ```

## Contributing
Guidelines for contributing to the project.
```

#### 2.5.2 Module Documentation
- **Module-level docstrings** explaining purpose
- **Function docstrings** with Args, Returns, Examples
- **Type hints** for all parameters and return values
- **Example code** in docstrings

### 2.6 Security Standards

#### 2.6.1 Secrets Management
- **Never commit** secrets to repository
- Use **.env** files for local development
- Use **GitHub Secrets** for CI/CD
- **Rotate credentials** regularly

#### 2.6.2 Input Validation
- **Validate all user inputs** in tools
- **Sanitize expressions** in calculator tool
- **Limit memory size** to prevent resource exhaustion
- **Session timeout** for memory cleanup

### 2.7 Performance Standards

#### 2.7.1 Memory Management
- **Limit session memory** to last 50 messages
- **Implement cleanup** for old sessions
- **Monitor memory usage** in production
- **Use connection pooling** for AWS clients

#### 2.7.2 Response Time
- **Chain execution** under 30 seconds
- **Tool execution** under 1 second
- **Memory operations** under 100ms
- **Implement timeouts** for external calls

## 3. Review Checklist

### 3.1 Pre-Commit Checklist
- [ ] Code follows PEP 8/Black formatting
- [ ] All tests pass locally
- [ ] No linting errors
- [ ] Type checking passes
- [ ] Documentation updated
- [ ] Commit message follows convention
- [ ] No secrets in code
- [ ] Feature flags removed if applicable

### 3.2 Pull Request Review Checklist
- [ ] Single responsibility principle followed
- [ ] Tests cover new functionality
- [ ] No breaking changes to existing API
- [ ] Documentation updated
- [ ] Code is readable and maintainable
- [ ] Performance considerations addressed
- [ ] Security considerations addressed
- [ ] Error handling implemented

### 3.3 Release Checklist
- [ ] All tests pass in CI/CD
- [ ] Version number updated
- [ ] CHANGELOG.md updated
- [ ] Documentation reviewed
- [ ] Dependency versions checked
- [ ] Security scan clean
- [ ] Performance tests pass

## 4. Monitoring and Maintenance

### 4.1 Logging Standards
```python
import logging

logger = logging.getLogger(__name__)

def chat_with_memory(message: str, session_id: str = "default") -> str:
    """Chat with memory-enabled bot."""
    logger.info(f"Chat request: session={session_id}, message={message[:50]}...")
    try:
        # Implementation
        logger.debug(f"Chat response: {response[:50]}...")
        return response.content
    except Exception as e:
        logger.error(f"Chat error: {str(e)}", exc_info=True)
        raise
```

### 4.2 Error Handling
- **Use specific exceptions** where possible
- **Provide helpful error messages**
- **Log errors with context**
- **Graceful degradation** when possible

### 4.3 Regular Maintenance Tasks
1. **Weekly**: Update dependencies, check security alerts
2. **Monthly**: Review and clean up old sessions/branches
3. **Quarterly**: Update documentation, review standards
4. **Annually**: Major dependency updates, architecture review

## 5. Quick Reference Commands

### 5.1 Development
```bash
# Setup
git clone <repo>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install

# Testing
pytest tests/ -v
pytest tests/ -v --cov=src --cov-report=html

# Linting
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/

# Running
python main.py
```

### 5.2 Git Operations
```bash
# Create feature branch
git checkout -b feature/new-chain

# Commit changes
git add .
git commit -m "feat(chains): add new chain implementation"

# Push to remote
git push origin feature/new-chain

# Create PR (using GitHub CLI)
gh pr create --title "Add new chain" --body "Description" --reviewer "team-lead"
```

