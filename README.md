# RAG-LLM Evaluation Testing Framework

> **A Robust, Flexible, and Beginner-Friendly Framework to Evaluate Retrieval-Augmented Generation (RAG) LLM Systems.**

---

## 🚀 What is this project?

This project helps you **evaluate how well large language models (LLMs)** (like GPT-4, Claude, Llama2, etc.) **perform on Retrieval-Augmented Generation (RAG) tasks**—such as answering questions using retrieved context from your documents.  
It supports **industry-standard metrics, full automation, rich reports, and plug-and-play support for new models or metrics**.

- **Built for:**
  - AI/ML engineers, QA/testers, and researchers
  - Data/product teams validating model upgrades or knowledge base changes
  - Beginners wanting to learn RAG LLM testing hands-on

---

## 🧩 Key Features

- **Automatic test case generation:** Feed your docs—generate, run, and score test cases (API/CSV/JSON or manual input).
- **Extensive metric coverage:** Faithfulness, factuality, fluency, hallucination, answer/context relevance/precision/recall, redundancy, helpfulness, instruction-following, completeness, named entities, and more.
- **Plug-and-play model support:** GPT-4, GPT-3.5, Claude, Llama, and your custom LLMs—just set config.
- **Rich, exportable reporting:** Interactive dashboard (Streamlit), CLI output, JSON/HTML reports, and PDF export.
- **No background needed:** Full step-by-step guide for first-time users and beginners.
- **Easily extensible:** Add new metrics, custom scorers, new models, or pipelines with simple config/code.
- **Robust test suite:** Pytest-based for total coverage, regression safety, and CI/CD integration.
- **Cross-platform:** Works on Windows, Mac, Linux (with instructions for each).
- **Beginner-friendly:** Simple setup and hand-holding docs.

---

## 📁 Project Structure (What’s in Each Folder?)

- `main.py` – The main CLI runner and orchestrator
- `utils/` – All helper utilities (logging, data loading, config, reporting, LLM wrappers, retry, etc.)
- `models/` – Model and metric configs, model capability mapping
- `tests/` – Pytest test suite for all metrics, coverage, and integrations
- `dashboard/` – Streamlit app for interactive result visualization and PDF export
- `examples/` – Demo scripts and sample usage
- `requirements.txt` – All dependencies for pip install

---

## 💻 How To Install and Launch (Step-by-Step for All OS)

### **1. Prerequisites**

- Python 3.9+ installed (`python --version`)
- `pip` for package installs
- (Optional) [Git](https://git-scm.com/) if cloning repo, or just download and extract zip

### **2. Clone or Download the Project**

**Using Git:**
```sh
git clone https://github.com/your-org/rag-llm-eval-testing-framework.git
cd rag-llm-eval-testing-framework

Or download the ZIP:
Download ZIP and unzip.

3. Create a Virtual Environment (Recommended, all OS)
Windows:

sh
Copy
Edit
python -m venv venv
venv\Scripts\activate
Mac/Linux:

sh
Copy
Edit
python3 -m venv venv
source venv/bin/activate
4. Install All Dependencies
sh
Copy
Edit
pip install -r requirements.txt
5. Configure Your Models and API Keys
Open config.json (in root folder) and edit to match your model provider and keys (OpenAI, Anthropic, local, etc.)

If using custom models, see models/model_capabilities.yaml for mapping and supported metrics.

For local LLMs, follow the instructions in the README_dev.md.

6. Add Your Test Data
Place your data files (CSV or JSON) in the appropriate location (see config).

Example CSV/JSON formats are provided in the tests/data/ folder.

To generate test cases from your own documents, use the provided scripts or follow the GUIDE_FOR_FRESHERS.md.

7. Run an Evaluation (CLI Example)
sh
Copy
Edit
python main.py --data tests/data/test_data.json --config config.json --output results/
For more options (e.g., selecting model/metrics/output format), run:

sh
Copy
Edit
python main.py --help
8. View Results (Interactive Dashboard)
sh
Copy
Edit
cd dashboard
streamlit run app.py
Open the dashboard link in your browser to view visualizations, trends, and export PDF reports.

🛠️ Models and Supported Metrics
Supported Models (out of the box):
GPT-4 / GPT-3.5 (OpenAI)

Claude (Anthropic)

Llama/Llama2 (local)

Custom LLMs (just set your provider/client in config)

Adding New Models:
Edit config.json and models/model_capabilities.yaml to register model, provider, and supported metrics.

Add new API keys (see .env.example).

Metric Support Matrix:
Each model’s supported metrics are mapped in model_capabilities.yaml.

The system will skip unsupported metrics automatically and report why (see HTML/JSON report).

🧪 Adding New Metrics or Custom Tests
New metric? Add its config in models/metric_config.py and code in utils/utils/scorer.py.

Custom test? Copy tests/templates/custom_metric_template.py and follow the instructions.

Register your metric in configs so it shows up in the dashboard and CLI.

🧑‍💻 Developer/Contributor Notes
See README_dev.md for full architecture, API, test, and extension instructions.

Run tests with:

sh
Copy
Edit
pytest tests/
For CI/CD integration, use the provided Jenkinsfile.

📊 Output & Reporting
CLI: Colorized, tabular, and summary output

JSON/HTML: Detailed, structured, and suitable for automation

Dashboard: Interactive plots, filtering, and PDF export

Artifacts: All results saved to results/ (or as configured)

🆘 Troubleshooting & FAQ
Q: I get a “ModuleNotFoundError” or “ImportError”
A: Activate your virtual environment and make sure dependencies are installed.

Q: “API key not found” error
A: Set your API keys in config.json or as environment variables.

Q: Dashboard won’t launch or no data?
A: Make sure your evaluations have produced results in the results/ or configured output folder.

Q: How do I add my own LLM or metric?
A: See the “Adding New Models/Metrics” section or README_dev.md.

Q: I want to learn from scratch!
A: Read the included GUIDE_FOR_FRESHERS.md.

📂 Folder-by-Folder Project Map
Folder/File	Purpose
main.py	Main CLI entrypoint, orchestrator
utils/	Utilities: logging, config, data loader, scorer, etc.
models/	Model/metric configs and capability mapping
tests/	Full test suite, templates, and test data
dashboard/	Streamlit web dashboard
examples/	Example scripts and usage
requirements.txt	Python dependencies
config.json	Global project and model config

👋 For Total Beginners
Don’t worry! Every step (from install to running to customizing) is in GUIDE_FOR_FRESHERS.md.

Just follow that file step-by-step if you have zero ML, coding, or CLI experience.

📣 Where to Get Help
Open an issue on GitHub

Email the maintainer listed in README_dev.md

See the FAQ above or GUIDE_FOR_FRESHERS.md
