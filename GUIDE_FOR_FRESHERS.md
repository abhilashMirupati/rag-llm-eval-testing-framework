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
