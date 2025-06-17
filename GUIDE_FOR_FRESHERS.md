# Guide for Newcomers to the RAG LLM Evaluation Framework

Welcome! This guide is designed to help you get started with the project quickly and effectively.

## 🚀 Quick Start

1.  **Setup Your Environment**:
    ```bash
    # Clone the repository
    git clone [https://github.com/yourusername/rag-llm-eval-testing-framework.git](https://github.com/yourusername/rag-llm-eval-testing-framework.git)
    cd rag-llm-eval-testing-framework

    # Use our setup script to create a virtual environment and install dependencies
    # This script handles Python, pip, requirements, and spaCy model installation.
    bash setup.sh

    # Activate the virtual environment
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

2.  **Configure Your API Keys**:
    -   Rename `.env.example` to `.env`.
    -   Open the `.env` file and add your API key for the LLM provider you want to use (e.g., `OPENAI_API_KEY`).

3.  **Run an Evaluation**:
    Use the command-line interface (CLI) to run your first evaluation. You'll need a dataset and a configuration file. We've provided examples.
    ```bash
    # Run the comprehensive example which creates temporary data and config
    python examples/comprehensive_evaluation.py
    ```
    This will generate reports in the `example_reports/` directory.

4.  **Explore the Dashboard**:
    The dashboard is the best way to visualize results.
    ```bash
    # Start the dashboard using the helper script
    bash dashboard.sh
    ```
    Now, open your web browser to `http://localhost:8501`.

## 📂 Project Structure

Here is a high-level overview of the project's structure:

rag-llm-eval-testing-framework/
├── dashboard/              # Streamlit dashboard application
│   └── app.py
├── examples/               # Example scripts showing how to use the framework
├── models/                 # Model and metric capability definitions
├── tests/                  # All test files (unit, integration)
├── utils/                  # Core framework utilities
│   ├── templates/          # HTML templates for reports
│   ├── config_manager.py   # Handles loading config.json
│   ├── data_loader.py      # Loads data from files (CSV, JSON)
│   ├── llm_wrapper.py      # Wrapper for LLM API calls
│   ├── metrics_manager.py  # Orchestrates metric calculations
│   ├── reporter.py         # Generates evaluation reports
│   └── scorer.py           # Contains the logic for all evaluation metrics
├── .env.example            # Example for environment variables (API keys)
├── config.json             # Main configuration file
├── main.py                 # Main function orchestrating the evaluation run
├── rag-eval-cli.py         # Command-Line Interface entry point
├── requirements.txt        # Project dependencies
└── README.md               # Main project documentation


## ✅ Common Tasks

### Running Evaluations from the CLI

The `rag-eval-cli.py` script is your main tool for running evaluations.

```bash
# Basic evaluation using default config and a specified data file
rag-eval --data_path tests/data/test_data.csv

# Override the model and metrics from the config file
rag-eval --data_path tests/data/test_data.csv --model_name "gpt-3.5-turbo" --metrics "faithfulness" "fluency"
Adding a New Metric
Implement Logic: Add a new evaluate_<your_metric_name> method to utils/utils/scorer.py.
Add Test: Create a new test file tests/tests/test_metrics/test_<your_metric_name>.py that inherits from BaseMetricTest.
Add Test Data: Add cases for your new metric to tests/data/test_data.json.
Update Config: Add your new metric's name to config.json to run it by default.
See CONTRIBUTING.md for more details.

troubleshoot
Dashboard Not Starting: Ensure you have activated the virtual environment (source .venv/bin/activate) and that port 8501 is free.
Tests Failing: Check that all dependencies are installed (pip install -r requirements.txt) and that your .env file is set up correctly.
LLM Connection Issues: Verify your API keys in the .env file are correct and that you have an active internet connection.
📚 Learning Resources
README.md: The main project overview.
CONTRIBUTING.md: Detailed guidelines for contributing.
examples/ directory: Practical, executable examples.
Welcome aboard, and we look forward to your contributions!


***

### `README.md`
```markdown
# RAG LLM Evaluation Framework

An advanced, extensible, and user-friendly framework for the comprehensive evaluation of Retrieval-Augmented Generation (RAG) systems.

![Dashboard Screenshot](https://user-images.githubusercontent.com/12345/67890.png) ## ✨ Features

-   **Comprehensive Metrics**: Over 15 built-in metrics including `faithfulness`, `answer_relevance`, `context_recall`, `fluency`, and `hallucination`.
-   **Broad LLM Support**: Seamlessly switch between models from providers like OpenAI, Anthropic, and local models.
-   **Interactive Dashboard**: A powerful Streamlit dashboard to visualize results, compare model performance, and track trends over time.
-   **Extensive Reporting**: Automatically generate detailed reports in multiple formats (HTML, JSON, PDF).
-   **Highly Extensible**: Easily add custom metrics and models with a clean, modular architecture.
-   **Robust Testing**: A comprehensive test suite using `pytest` ensures reliability and correctness.
-   **Developer Friendly**: Comes with a CLI, detailed documentation, and setup scripts for a smooth development experience.

## 🚀 Quick Start

1.  **Setup Environment**:
    Our setup script handles everything from creating a virtual environment to installing dependencies and required models.
    ```bash
    bash setup.sh
    ```

2.  **Activate Environment**:
    ```bash
    source .venv/bin/activate
    ```

3.  **Configure API Keys**:
    ```bash
    cp .env.example .env
    # Now, edit the .env file with your API keys
    ```

4.  **Run a Sample Evaluation**:
    Use the command-line tool to run an evaluation on the provided sample data.
    ```bash
    rag-eval --data_path tests/data/test_data.csv --config_path config.json --output_dir reports
    ```

5.  **Launch the Dashboard**:
    ```bash
    bash dashboard.sh
    ```
    Navigate to `http://localhost:8501` in your browser to see the results.

## 📂 Project Structure

rag-llm-eval-testing-framework/
├── dashboard/              # Streamlit dashboard application
├── examples/               # Example scripts
├── models/                 # Model and metric capability definitions
├── tests/                  # All test files
├── utils/                  # Core framework utilities
│   ├── templates/          # HTML templates for reports
│   ├── config_manager.py   # Handles configuration
│   ├── data_loader.py      # Loads datasets
│   ├── llm_wrapper.py      # Wrapper for LLM APIs
│   ├── metrics_manager.py  # Orchestrates metric evaluation
│   ├── reporter.py         # Generates reports
│   └── scorer.py           # Core logic for all metrics
├── .env.example            # Example for environment variables
├── config.json             # Main configuration file
├── main.py                 # Main evaluation orchestrator
├── rag-eval-cli.py         # Command-Line Interface
├── requirements.txt        # Project dependencies
└── README.md               # This file


## Documentation

-   [**Guide for Newcomers**](GUIDE_FOR_FRESHERS.md): Your starting point for using the framework.
-   [**Contributing Guidelines**](CONTRIBUTING.md): Learn how to contribute to the project.
-   [**Developer Guide**](README_dev.md): In-depth guide for advanced development.
-   [**Code of Conduct**](CODE_OF_CONDUCT.md): Our community standards.

## 🤝 Contributing

We welcome contributions of all kinds! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get started.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

