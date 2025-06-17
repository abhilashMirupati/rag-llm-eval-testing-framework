# Contributing to RAG-LLM Evaluation Framework

Thank you for your interest in contributing to the RAG-LLM Evaluation Framework! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### 1. Fork and Clone

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/yourusername/rag-llm-eval.git
cd rag-llm-eval
```

### 2. Set Up Development Environment

1. Install Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Set up pre-commit hooks:
```bash
poetry run pre-commit install
```

### 3. Create a Branch

Create a new branch for your feature or fix:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-fix-name
```

### 4. Make Changes

1. Write your code following our style guide
2. Add tests for new features
3. Update documentation
4. Run tests locally:
```bash
poetry run pytest
```

### 5. Commit Changes

Follow our commit message format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance

Example:
```
feat(metrics): add new factuality metric

- Implemented new factuality scoring
- Added tests
- Updated documentation

Closes #123
```

### 6. Push and Create Pull Request

1. Push your changes:
```bash
git push origin feature/your-feature-name
```

2. Create a Pull Request on GitHub
3. Fill out the PR template
4. Request review from maintainers

## Development Guidelines

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings
- Keep functions small and focused
- Use meaningful variable names

### Testing

- Write unit tests for all new code
- Maintain test coverage
- Use fixtures for common setup
- Test edge cases
- Run tests before committing

### Documentation

- Update README.md for user-facing changes
- Update README_dev.md for developer-facing changes
- Document API changes
- Add examples for new features
- Keep comments up to date

### Pull Request Process

1. Update documentation
2. Add tests
3. Ensure all tests pass
4. Update changelog
5. Get code review
6. Address review comments
7. Merge only after approval

## Adding New Features

### New Metrics

1. Create test file in `tests/`
2. Add implementation in `utils/scorer.py`
3. Update configuration
4. Add documentation
5. Add tests

### New Model Support

1. Create parser in `parsers/`
2. Update model configuration
3. Add tests
4. Update documentation

### Dashboard Features

1. Add visualization in `dashboard/app.py`
2. Update UI components
3. Add tests
4. Update documentation

## Reporting Issues

1. Use the issue template
2. Provide detailed description
3. Include steps to reproduce
4. Add error messages
5. Include environment details

## Review Process

1. Code review by maintainers
2. Automated checks must pass
3. Documentation review
4. Test coverage check
5. Final approval

## Release Process

1. Update version number
2. Update changelog
3. Create release notes
4. Tag release
5. Deploy

## Getting Help

- Check documentation
- Join our community
- Ask in issues
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License. 