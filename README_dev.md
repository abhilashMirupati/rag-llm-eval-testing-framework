# RAG-LLM Evaluation Testing Framework – Developer & Maintainer Guide

**This is the comprehensive guide for developers, maintainers, and contributors to the RAG-LLM Evaluation Testing Framework.**  
It explains the project’s internal structure, extension points, best practices, developer workflow, and advanced configuration.

---

## Table of Contents

- [1. Overview & Philosophy](#overview--philosophy)
- [2. Architecture & Project Structure](#architecture--project-structure)
- [3. Core Components Explained](#core-components-explained)
- [4. Adding New Models, Metrics, and Test Cases](#adding-new-models-metrics-and-test-cases)
- [5. Extending the Framework (Code, Config, API)](#extending-the-framework-code-config-api)
- [6. Local LLM & Custom Model Support](#local-llm--custom-model-support)
- [7. Developer Workflow & Testing](#developer-workflow--testing)
- [8. Continuous Integration (CI) & Jenkins](#continuous-integration-ci--jenkins)
- [9. Debugging, Troubleshooting, and Best Practices](#debugging-troubleshooting-and-best-practices)
- [10. Contribution Guidelines](#contribution-guidelines)
- [11. Support & Maintainer Info](#support--maintainer-info)

---

## 1. Overview & Philosophy

This framework is designed to **enable robust, scalable, and reproducible evaluation of RAG pipelines and LLM-based retrieval systems**.  
**Everything is modular:** new models, metrics, and reporting can be plugged in with minimal friction, while core evaluation flows are production-grade.

- **No logic is ever trimmed from user/contributor code.**
- **Tests, metrics, and configs are all explicit and traceable.**
- **Designed for:**
  - Automated CI/CD integration
  - Easy onboarding of new contributors
  - Real-world, large-scale LLM/RAG evaluation

---

## 2. Architecture & Project Structure

The project follows a clear, layered design for **traceability, reliability, and extensibility**.

rag-llm-eval-testing-framework/
│
├── main.py # Main CLI entrypoint and orchestrator
├── utils/ # Utilities: logging, config, data loading, scorer, wrappers
│ └── utils/ # Sub-utilities: LLM wrappers, retry, templates, etc.
├── models/ # Model/metric configs and model capability matrix
├── tests/ # Pytest suite for all metrics, regression, and integration
│ └── tests/ # Metric-by-metric tests (one class/file per metric)
│ └── utils/ # Test utilities, fixtures, and test data loading
├── dashboard/ # Streamlit dashboard for interactive analysis and export
├── examples/ # Example evaluation scripts and demo configs
├── requirements.txt # All dependencies
├── config.json # Global configuration file for models, data, and output
├── Jenkinsfile # Jenkins pipeline for CI/CD (test, lint, coverage, etc.)
├── README.md # End-user documentation and installation guide
├── README_dev.md # (This file) Developer/contributor/internal documentation
└── GUIDE_FOR_FRESHERS.md # Beginner step-by-step setup guide



---

## 3. Core Components Explained

### **main.py**
- **The main orchestrator:**  
  - Parses CLI arguments
  - Loads configs, models, and test data
  - Instantiates all core managers (Config, Metrics, Reporter, Scorer)
  - Runs the full evaluation loop and triggers reporting

### **utils/**
- **Helper utilities:**  
  - `logger.py` — project-wide logging setup
  - `data_loader.py` — loads CSV/JSON test cases
  - `config_manager.py` — parses and validates configs (config.json, YAML, etc.)
  - `metrics_manager.py` — connects test cases, metric configs, and scoring
  - `reporter.py` — builds and exports CLI, HTML, JSON, and PDF reports
  - `scorer.py` — implements all evaluation metric functions, wrapping RAGAS, DeepEval, and custom logic
  - `llm_wrapper.py` — safe, retryable API for OpenAI/Anthropic/Local/Custom models

### **models/**
- `model_config.py` — Model-specific settings, config parsing, and capability checks
- `metric_config.py` — Metric definition, required fields, and validation logic
- `model_capabilities.yaml` — Matrix mapping each model to supported metrics (add new models here)

### **tests/**
- **Comprehensive pytest suite:**  
  - `tests/tests/` — One file/class per metric, each with full batch and edge case coverage
  - `tests/utils/` — Shared test data handlers, fixtures, config utilities, data loader
  - `tests/templates/` — Template files for easily adding new metrics/tests

### **dashboard/**
- **Streamlit dashboard:**  
  - Loads SQLite or CSV results
  - Provides interactive trend analysis, metric filtering, PDF export, and summary stats

### **examples/**
- Demo evaluation scripts and walkthroughs for new users

---

## 4. Adding New Models, Metrics, and Test Cases

### **Add a New Model (Cloud or Local):**
1. **Add model to `models/model_capabilities.yaml`:**
   ```yaml
   models:
     my-llama:
       provider: local
       supported_metrics: [faithfulness, factuality, fluency, ...]


Add API key/config section in config.json:

json
Copy
Edit
{
  "models": {
    "my-llama": {
      "type": "local",
      "path": "/path/to/model",
      "params": {...}
    }
  }
}
If using a new provider:
Implement a new class in utils/llm_wrapper.py (subclassing or following the interface for get_completion()).

Add a New Metric:
Define it in models/metric_config.py:

python
Copy
Edit
class MetricConfig:
    ...
# Add your metric’s config
Implement logic in utils/scorer.py:

python
Copy
Edit
def evaluate_my_metric(self, answer, context, ...):
    # Metric logic here
    return EvaluationResult(score, details)
Register sample data for tests in tests/data/ (JSON or CSV).

Create a test file in tests/tests/ (copy from template).

Update metric mapping in model_capabilities.yaml if needed.

Add a New Test Case:
Add your case in the relevant JSON/CSV in tests/data/

Use proper metric name as used in the scorer/config

5. Extending the Framework (Code, Config, API)
To add a new report/export format:
Extend reporter.py, implement new method, and update CLI/config to allow it.

To add a new LLM provider:
Extend llm_wrapper.py and update config/CLI to allow user to select it.

To add custom CLI flags:
Update argument parsing in main.py, document the flag, and pass values to relevant modules.

6. Local LLM & Custom Model Support
Supported local models: Llama, Llama2, and any HuggingFace-compatible model.

For local inference:

Set "type": "local" and "path" in config.json.

Ensure your machine has enough resources (RAM, GPU if needed).

For running local server (e.g., vLLM, llamacpp, text-generation-webui), set the API endpoint in config.

Tip:
Use llm_wrapper.py as your integration point for all local and custom inference.

7. Developer Workflow & Testing
Setup
sh
Copy
Edit
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
Run All Tests
sh
Copy
Edit
pytest tests/
Check Lint, Type, and Coverage
sh
Copy
Edit
flake8 .
black --check .
mypy .
pytest --cov=utils --cov=models --cov=main tests/
Development Best Practices
Use the provided templates in tests/templates/ for new metrics or test cases.

Ensure all logic, even edge cases, is tested—never trim coverage for speed.

Check all code against existing metrics/tests before major refactors.

Always update or extend the test suite if adding new features.

8. Continuous Integration (CI) & Jenkins
Pipeline defined in Jenkinsfile (see also test_jenkins_pipeline.py for pipeline tests).

Stages:

Checkout

Lint (flake8, pylint, black, mypy)

Test (pytest)

Coverage

Build/Deploy (if configured)

Artifact collection (HTML/JSON reports, coverage.xml, etc.)

Notifications (Slack, Teams, email—if credentials set)

9. Debugging, Troubleshooting, and Best Practices
If you hit “ModuleNotFoundError”:

Check your virtual environment and PYTHONPATH.

“API key not found”:

Check env vars and config.json.

For local models, make sure path is set and model files exist.

Tests failing unexpectedly?

Run pytest tests/ --maxfail=1 -v and check stack trace.

Compare your test data and config mapping—metrics must match model capability.

Adding a new metric or model and seeing “not supported” warnings?

Update model_capabilities.yaml for your new entries.

Performance slow?

Use smaller test data, batch calls, or run on a machine with more memory/CPU.

Dashboard not loading?

Ensure streamlit is installed, output data exists, and browser cache is clear.

10. Contribution Guidelines
Fork and branch before making changes.

Always extend or add to the test suite for new features.

Use clear docstrings and comments—code should be readable by future maintainers.

Never trim logic or edge cases:

Coverage, robustness, and test traceability are top priorities.

Run all tests and lint before submitting a PR.

Document all new flags, metrics, or model support in README.md and/or here.

11. Support & Maintainer Info
For questions or bugs, open an issue in GitHub or contact the project maintainer (see project page).

For major contributions, review the CI logs and project status before submitting.

To join as a maintainer, reach out via the repo contact email.

Thank you for helping keep this project robust, reproducible, and production-ready!

yaml
Copy
Edit

---

**When you say “done,”  
I’ll deliver the final file:  
**`GUIDE_FOR_FRESHERS.md` – a truly beginner, step-by-step, hand-holding guide!**
