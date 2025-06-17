# RAG-LLM Evaluation Framework - Developer Guide

This guide provides in-depth information for developers working on the framework's core components.

## 🏗️ Architectural Overview

The framework is designed with a modular architecture to ensure separation of concerns and extensibility.

-   **`rag-eval-cli.py`**: The entry point for command-line operations. It uses `argparse` to parse arguments and calls `run_evaluation` in `main.py`.
-   **`main.py`**: The central orchestrator. It uses the various manager classes to coordinate the evaluation workflow: config -> data loading -> evaluation -> reporting.
-   **`utils/config_manager.py`**: Handles loading and providing access to settings from `config.json`.
-   **`utils/data_loader.py`**: Responsible for loading evaluation datasets from different file formats.
-   **`utils/metrics_manager.py`**: Iterates through the metrics defined in the config and calls the appropriate methods in the `Scorer`.
-   **`utils/scorer.py`**: The heart of the evaluation logic. Each metric has its own `evaluate_<metric_name>` method. This is where the actual computation happens.
-   **`utils/reporter.py`**: Takes the final results and generates reports in various formats (HTML, JSON, PDF) using templates.
-   **`dashboard/app.py`**: A self-contained Streamlit application for visualizing results stored in the database.

## 🛠️ Development Setup

1.  **Prerequisites**: Python 3.9+ and Poetry.
2.  **Installation**:
    ```bash
    # Clone the repository
    git clone [https://github.com/yourusername/rag-llm-eval-testing-framework.git](https://github.com/yourusername/rag-llm-eval-testing-framework.git)
    cd rag-llm-eval-testing-framework

    # Install dependencies using Poetry
    poetry install

    # Install pre-commit hooks for automated code quality checks
    poetry run pre-commit install
    ```
3.  **Environment Variables**:
    Copy `.env.example` to `.env` and fill in your API keys. The framework loads these variables automatically.
    ```bash
    cp .env.example .env
    ```

## 🧪 Running Tests

-   **Run all tests**:
    ```bash
    poetry run pytest
    ```
-   **Run a specific test file**:
    ```bash
    poetry run pytest tests/tests/test_metrics/test_faithfulness.py
    ```
-   **Run tests with coverage report**:
    ```bash
    poetry run pytest --cov=utils
    ```

## 📈 Adding a New Metric

Follow these steps to add a new metric called `your_metric`:

1.  **Implement the Logic in `Scorer`**:
    Open `utils/utils/scorer.py` and add a new method. It must accept the necessary inputs (e.g., answer, context) and return an `EvaluationResult` object.

    ```python
    # In utils/utils/scorer.py
    from .scorer import EvaluationResult

    def evaluate_your_metric(self, answer: str, context: str) -> EvaluationResult:
        # Your logic here
        score = 0.9 # Calculate the score
        details = "Your metric evaluation was successful."
        return EvaluationResult(score=score, details=details)
    ```

2.  **Add a Test File**:
    Create a new file `tests/tests/test_metrics/test_your_metric.py`. Use the `BaseMetricTest` class to minimize boilerplate.

    ```python
    # In tests/tests/test_metrics/test_your_metric.py
    from tests.utils.base_metric_test import BaseMetricTest
    # ... other imports

    class TestYourMetric(BaseMetricTest):
        metric_name = "your_metric"

        def run_evaluation(self, test_case: dict) -> EvaluationResult:
            # Extract inputs and call the scorer method
            answer = test_case["answer"]
            context = test_case["context"]
            return self.scorer.evaluate_your_metric(answer, context)

        @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
        def test_your_metric_logic(self, test_case: dict):
            self.test_metric_logic(test_case)
    ```

3.  **Add Test Data**:
    Open `tests/data/test_data.json` and add test cases for your new metric.

    ```json
    "your_metric": [
      {
        "answer": "An example answer.",
        "context": "An example context.",
        "expected_min_score": 0.8
      }
    ]
    ```

4.  **Update `MetricsManager`**:
    Open `utils/utils/metrics_manager.py` and ensure the `evaluate_metrics` method correctly passes the required arguments to your new scorer method. You may need to add a new condition.

5.  **(Optional) Add to `config.json`**:
    To run your new metric by default, add `"your_metric"` to the `metrics` list in `config.json`.

## 🤖 Adding New Model Support

1.  **Update `LLMWrapper`**:
    If the new model uses a different API provider, add logic to `utils/utils/llm_wrapper.py` to initialize its client and handle its `get_completion` request/response format.

2.  **Update `ResponseParser`**:
    Add a new `parse_<provider>` method to `utils/utils/response_parser.py` to transform the new model's raw response into a standardized `ParsedResponse` object.

3.  **Update `model_capabilities.yaml`**:
    Add the new model and its supported metrics to `models/model_capabilities.yaml`.

4.  **Add to `config.json`**:
    You can now specify the new model in your `config.json` to use it for evaluations.
