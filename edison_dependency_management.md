# Project Documentation: Dependency & Environment Management

## 1. Dependency and Environment Management

### 1.1 Project Structure
```
langchain-assistant/
├── .github/
│   └── workflows/
│       ├── lint.yml
│       └── test.yml
├── src/
│   ├── __init__.py
│   ├── client.py
│   ├── prompts.py
│   ├── chains.py
│   ├── memory.py
│   └── tools.py
├── tests/
│   ├── __init__.py
│   ├── test_client.py
│   ├── test_prompts.py
│   ├── test_chains.py
│   ├── test_memory.py
│   └── test_tools.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── README.md
└── main.py
```

### 1.2 Dependency Files

**requirements.txt:**
```txt
langchain>=0.1.0
langchain-aws>=0.1.0
langchain-core>=0.1.0
boto3>=1.28.0
python-dotenv>=1.0.0
```

**requirements-dev.txt:**
```txt
-r requirements.txt
pytest>=7.0.0
pytest-cov>=4.0.0
flake8>=6.0.0
black>=23.0.0
isort>=5.12.0
mypy>=1.0.0
pre-commit>=3.0.0
```

**pyproject.toml:**
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 88
target-version = ['py310']
include = '\.pyi?$'
extend-exclude = '''
/(
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### 1.3 Environment Setup

**Initial Setup:**
```bash
# Clone repository
git clone <repository-url>
cd langchain-assistant

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Copy environment template
cp .env.example .env
# Edit .env with your AWS credentials
```

**Environment Variables (.env.example):**
```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# Model Configuration
MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
TEMPERATURE=0.1
MAX_TOKENS=1024

# Application Configuration
DEBUG=true
LOG_LEVEL=INFO
```

### 1.4 Development Workflow

**Daily Development:**
```bash
# Activate environment
source .venv/bin/activate

# Run tests
pytest tests/ -v --cov=src

# Run linting
flake8 src/ tests/
black src/ tests/
isort src/ tests/

# Run type checking
mypy src/

# Run all checks
pre-commit run --all-files
```

**Dependency Updates:**
```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade <package-name>

# Update requirements files
pip freeze > requirements.txt
# Manually review and update requirements-dev.txt
```
