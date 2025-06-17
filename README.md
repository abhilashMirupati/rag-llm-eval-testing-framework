# RAG LLM Evaluation Framework

A comprehensive, production-ready framework for evaluating Retrieval-Augmented Generation (RAG) systems with various Large Language Models (LLMs).

## Key Features

- **Comprehensive Metrics:** Includes a suite of metrics for evaluating faithfulness, relevance, fluency, and more.
- **Multi-LLM Support:** Easily switch between providers like OpenAI and Anthropic.
- **Data-Driven:** Configure and run evaluations using simple JSON or CSV files.
- **Automated Reporting:** Generate detailed evaluation reports in JSON and HTML formats.
- **Interactive Dashboard:** Visualize results and trends with a built-in Streamlit dashboard.
- **Extensible:** Designed to be easily extended with new metrics and models.

## Quick Start

1.  **Set Up Environment:**
    Run the setup script to create a virtual environment and install all dependencies.
    ```bash
    ./setup.sh
    ```

2.  **Configure API Keys:**
    Rename `.env.example` to `.env` and add your API keys.
    ```bash
    mv .env.example .env
    # Now, edit the .env file with your keys
    ```

3.  **Configure Evaluation:**
    Edit `config.json` to define which model and metrics you want to run.

4.  **Run Evaluation:**
    Execute the command-line tool with the path to your data.
    ```bash
    python rag-eval-cli.py --data_path path/to/your/data.csv
    ```

5.  **View Results:**
    - Check the `reports/` directory for JSON and HTML reports.
    - Launch the interactive dashboard: `./dashboard.sh`

## Project Structure
