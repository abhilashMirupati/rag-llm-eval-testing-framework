# Contributing to the RAG-LLM Evaluation Framework

First off, thank you for considering contributing! Your help is essential for keeping this project great. This document provides guidelines to ensure a smooth and effective contribution process.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

There are many ways to contribute, from writing code and documentation to reporting bugs and suggesting new features.

### Reporting Bugs

- **Ensure the bug was not already reported** by searching on GitHub under [Issues](https://github.com/yourusername/rag-llm-eval-testing-framework/issues).
- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/yourusername/rag-llm-eval-testing-framework/issues/new). Be sure to include a **title and clear description**, as much relevant information as possible, and a **code sample or an executable test case** demonstrating the expected behavior that is not occurring.

### Suggesting Enhancements

- Open a new issue to discuss your enhancement. Clearly describe the proposed enhancement, its use case, and provide examples if possible.
- This allows for community feedback and ensures your work aligns with the project's goals before you invest a lot of time.

### Pull Requests

1.  **Fork and Clone**: Fork the repository and clone it locally. Connect your local to the original "upstream" repository by adding it as a remote.
2.  **Create a Branch**: Create a new branch from `main` for your changes. Use a descriptive name like `feature/new-metric-name` or `fix/dashboard-bug`.
3.  **Set Up Environment**: Use Poetry to set up your development environment.
    ```bash
    # Install dependencies
    poetry install
    # Activate pre-commit hooks
    poetry run pre-commit install
    ```
4.  **Make Changes**: Write your code. Ensure it follows our style guidelines and that all tests pass.
5.  **Add Tests**: If you add new functionality, you must add tests. If you fix a bug, add a test that catches the bug.
6.  **Update Documentation**: Update any relevant documentation (`README.md`, `README_dev.md`, docstrings, etc.).
7.  **Commit and Push**: Follow our commit message format (see below). Push your changes to your fork.
8.  **Create a Pull Request**: Open a pull request to the `main` branch of the upstream repository. Provide a clear description of the changes and link to any relevant issues.

## Development Guidelines

### Code Style
- We follow **PEP 8** for Python code.
- We use **Black** for code formatting, **isort** for import sorting, and **Flake8** for linting. These are enforced by the pre-commit hooks.
- **Type hints** are required for all function signatures.
- **Docstrings** should follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. This helps in automating changelog generation and makes the project history easier to read.

Format: `type(scope): description`

-   **Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `build`.
-   **Scope** (optional): The part of the codebase you're changing (e.g., `scorer`, `dashboard`, `config`).

Example:
`feat(scorer): add new answer_similarity metric`

### Testing
- All new code must be accompanied by tests.
- We use `pytest`. Run tests locally with `poetry run pytest`.
- Aim for high test coverage. Check coverage with `poetry run pytest --cov`.

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.
