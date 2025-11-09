# Contributing to ARC Adaptors

Thank you for your interest in contributing to the ARC Adaptors library! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)
- [Release Process](#release-process)

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, or poetry)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/arc-adaptors.git
   cd arc-adaptors
   ```

## Development Setup

### 1. Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Using conda
conda create -n arc-adaptors python=3.11
conda activate arc-adaptors
```

### 2. Install Development Dependencies

```bash
# Install in development mode with all extras
pip install -e ".[dev]"
```

### 3. Verify Installation

```bash
# Run tests
pytest

# Check code style
black --check .
flake8 .
mypy arc_adaptors/
```

## Contributing Guidelines

### Types of Contributions

We welcome the following types of contributions:

- **🐛 Bug fixes** - Fix issues in existing adaptors
- **✨ New adaptors** - Add new adaptors for frameworks or services
- **📚 Documentation** - Improve docs, examples, or guides
- **🧪 Tests** - Add or improve test coverage
- **🎨 Code quality** - Refactoring, performance improvements
- **🔧 Tooling** - CI/CD, development tools, automation

### Before You Start

1. **Search existing issues** - Check if your bug/feature is already reported
2. **Open an issue** - Discuss significant changes before implementing
3. **Check roadmap** - Ensure your contribution aligns with project goals

### Adaptor Implementation Guidelines

When contributing new adaptors or modifying existing ones, ensure:

- **Consistency**: Follow the BaseAdaptor interface
- **Error Handling**: Provide meaningful error messages and proper exception handling
- **Documentation**: Include clear examples of how to use the adaptor
- **Testing**: Comprehensive tests for the adaptor functionality
- **Dependencies**: Clearly mark framework-specific dependencies as optional

## Pull Request Process

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number
```

### 2. Make Changes

- Follow [Code Style](#code-style) guidelines
- Add/update tests for your changes
- Update documentation if needed
- Ensure all tests pass

### 3. Commit Changes

Use conventional commits format:
```bash
git commit -m "feat: add anthropic adaptor implementation"
git commit -m "fix: handle streaming responses in langchain adaptor"
git commit -m "docs: update examples for openai adaptor"
```

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title and description
- Link to related issues
- Description of changes made
- Testing performed

## Code Style

### Python Style

We use the following tools for code quality:

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type checking
mypy arc_adaptors/
```

### Code Guidelines

- **Type hints**: Use type hints for all public APIs
- **Docstrings**: Use Google-style docstrings
- **Error handling**: Provide meaningful error messages
- **Logging**: Use structured logging with appropriate levels

### Example Code Style

```python
from typing import Optional, Dict, Any
from arc_adaptors.base import BaseAdaptor

class ExampleAdaptor(BaseAdaptor):
    """Example adaptor for integrating with Service X.
    
    This adaptor provides translation between ARC Protocol and Service X API.
    
    Args:
        api_key: Service X API key
        endpoint: Service X endpoint URL
        config: Additional configuration options
    """
    
    def __init__(
        self, 
        api_key: str, 
        endpoint: str, 
        config: Optional[Dict[str, Any]] = None
    ) -> None:
        self.api_key = api_key
        self.endpoint = endpoint
        super().__init__(config)
        
    def _validate_config(self) -> None:
        """Validate the adaptor configuration."""
        if not self.api_key:
            raise ValueError("API key is required")
```

## Testing

### Test Structure

```
tests/
├── test_base.py           # Tests for base adaptor
├── test_langchain_adaptor.py  # Tests for LangChain adaptor
├── test_openai_adaptor.py     # Tests for OpenAI adaptor
└── ...
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_langchain_adaptor.py

# Run with coverage
pytest --cov=arc_adaptors --cov-report=html
```

### Writing Tests

- Use `pytest` framework
- Mock external dependencies
- Test both success and error cases
- Include adaptor-specific edge cases

```python
import pytest
from arc_adaptors.langchain import ARCLangChainAdaptor

@pytest.mark.asyncio
async def test_load_tools_success():
    """Test successful tool loading."""
    adaptor = ARCLangChainAdaptor(
        arc_endpoint="https://test.arc",
        ledger_url="https://test.ledger",
        agent_ids=["test-agent"]
    )
    
    # Mock the necessary components
    with patch(...) as mock_load:
        mock_load.return_value = [...]
        
        tools = await adaptor.load_tools()
        
        assert len(tools) == 1
        assert tools[0].name == "transfer_to_test_agent"
```

## Documentation

### Types of Documentation

- **API Reference** - Auto-generated from docstrings
- **User Guide** - Step-by-step tutorials for each adaptor
- **Examples** - Real-world usage patterns

### Writing Documentation

- Use clear, concise language
- Include code examples for each adaptor
- Update docstrings for new/changed APIs
- Add examples to `examples/` directory

## Issue Reporting

### Bug Reports

Please include:

- **Environment**: Python version, OS, arc-adaptors version
- **Steps to reproduce**: Minimal code example
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Logs/errors**: Full error messages and stack traces

### Feature Requests

Please include:

- **Use case**: Why is this adaptor/feature needed?
- **Proposed solution**: How should it work?
- **Alternatives**: Other ways to solve the problem
- **Framework details**: Version requirements, compatibility concerns

## Release Process

### Version Numbering

We follow semantic versioning (SemVer):
- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes (backward compatible)

### Release Checklist

1. Update version in `pyproject.toml` and `setup.py`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Create release PR
5. Tag release: `git tag v1.2.3`
6. Build and publish to PyPI
7. Create GitHub release

### Publishing to PyPI

```bash
# Build package
python -m build

# Test on TestPyPI first
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## License

By contributing to ARC Adaptors, you agree that your contributions will be licensed under the Apache License 2.0.

---

Thank you for contributing to the ARC Protocol ecosystem! 🚀