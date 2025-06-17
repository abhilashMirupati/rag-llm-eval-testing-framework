.PHONY: install test lint format clean docs

install:
	poetry install

test:
	poetry run pytest

lint:
	poetry run flake8 .
	poetry run mypy .
	poetry run black . --check
	poetry run isort . --check-only

format:
	poetry run black .
	poetry run isort .

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs:
	poetry run mkdocs build

serve-docs:
	poetry run mkdocs serve

run-dashboard:
	poetry run streamlit run dashboard/app.py

setup-pre-commit:
	poetry run pre-commit install

update-deps:
	poetry update

build:
	poetry build

publish:
	poetry publish

docker-build:
	docker build -t rag-llm-eval .

docker-run:
	docker run -p 8501:8501 rag-llm-eval 