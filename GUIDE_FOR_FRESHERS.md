# GUIDE_FOR_FRESHERS.md

> **A Step-by-Step Beginner’s Guide to Setting Up and Using the RAG-LLM Evaluation Testing Framework**

---

## What is this Framework?

This framework helps you **test and compare the accuracy and reliability of large language models (LLMs)** when answering questions based on your own documents.  
It’s built for anyone: **total beginners, students, QA engineers, or data scientists**—no deep ML or coding knowledge required!

---

## 🌱 Getting Started – The Fast Path

### 1. **Install Python**

- You need **Python 3.9 or later**.
- Download it here: [python.org/downloads](https://www.python.org/downloads/).
- To check, open a terminal or command prompt and type:
  ```sh
  python --version


  If it prints something like Python 3.10.5, you’re good!

2. Download the Project
Go to the GitHub repo (your-org/rag-llm-eval-testing-framework)

Click the green “Code” button, then “Download ZIP.”

Unzip/extract it to a folder on your computer.

3. Open Your Terminal or Command Prompt
On Windows: Press Win+R, type cmd, and press Enter.

On Mac/Linux: Open Terminal from Applications or with Spotlight.

Navigate to your project folder:

sh
Copy
Edit
cd path/to/rag-llm-eval-testing-framework
(Replace path/to with where you extracted the project.)

4. Set Up a Virtual Environment (Recommended)
This keeps all project dependencies in one place.

Type:

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
You should see (venv) in your terminal—this means the environment is active.

5. Install All Required Packages
sh
Copy
Edit
pip install -r requirements.txt
This will install all the Python packages you need for the framework to work.

6. Configure Model API Keys and Settings
If you want to use GPT-4, Claude, or other cloud models, you’ll need an API key (ask your team or sign up with the provider).

Open the file config.json in Notepad, VSCode, or any text editor.

Paste your API keys or set your model path if using a local LLM.

Double-check the model names and supported metrics in models/model_capabilities.yaml.

7. Prepare Your Test Data
You can use the example data in tests/data/test_data.json or tests/data/test_data.csv.

To add your own questions/answers/contexts, just edit or copy these files—keep the format the same!

8. Run Your First Evaluation
sh
Copy
Edit
python main.py --data tests/data/test_data.json --config config.json --output results/
(Change the file paths if your data/config are elsewhere)

What happens?

The script reads your test cases.

It asks your chosen model(s) to answer each question using the context.

It runs dozens of tests and scores the answers using built-in metrics.

It saves the results to the results/ folder.

9. See Your Results
For quick results, look at the results/ folder—JSON and HTML reports are generated.

To get a beautiful dashboard:

sh
Copy
Edit
cd dashboard
streamlit run app.py
Click the link that appears, and you’ll get charts, tables, PDF export, and more!

🏆 What Metrics Are Measured?
Faithfulness: Did the model stay true to the source context?

Factuality: Is the answer actually correct?

Fluency: Is it written in clear, proper language?

Hallucination: Did it “make up” info not in the docs?

Relevance: Did it answer the question or wander off-topic?

Helpfulness, redundancy, conciseness, completeness, instruction following, and more!

All metrics are scored from 0 (bad) to 1 (perfect), and most reports explain the details.

🧑‍🔬 How to Add Your Own Test Cases
Open tests/data/test_data.json (or .csv) in a text editor.

Add new entries, keeping the same keys as in the examples:

json
Copy
Edit
{
  "question": "Who wrote Hamlet?",
  "context": ["William Shakespeare wrote Hamlet."],
  "answer": "Hamlet was written by Shakespeare."
}
Save the file and re-run the evaluation.

The system will automatically pick up your new tests!

🤖 How to Add or Switch Models
Edit config.json to change which model to use.

See models/model_capabilities.yaml to check which metrics each model supports.

If you want to use a local (offline) model, follow the README_dev.md for setup tips.

🛠️ Troubleshooting & Common Problems
Q: It says "ModuleNotFoundError" or “No module named X”

Did you run pip install -r requirements.txt in your virtual environment?

Make sure your (venv) is activated in the terminal.

Q: “API key not found”

Open config.json and make sure your key is present.

Or set it as an environment variable:
On Windows:

sh
Copy
Edit
set OPENAI_API_KEY=sk-xxxxx
On Mac/Linux:

sh
Copy
Edit
export OPENAI_API_KEY=sk-xxxxx
Q: Dashboard shows no results

Run main.py first so results are generated.

Make sure the output folder in your command matches what the dashboard expects.

Q: Something else is wrong

Check the error message—it usually tells you what’s missing.

Ask a teammate or open an issue on GitHub.

🏁 Next Steps
Try editing the test data or config and see how your scores change.

Explore the dashboard to compare different models or questions.

To go deeper, see the main README.md or README_dev.md for advanced features.

💡 Tips for Total Beginners
You can’t break anything! If you make a mistake, just delete and unzip the project again.

You don’t need to know code—just follow the steps above and edit the data/config files as shown.

Every file has comments or sample entries to help you.

If you want to learn how it works “under the hood,” read README_dev.md for technical details.

🆘 Still stuck?
Ask for help on GitHub, send an email to the maintainer, or share your error message with a teammate.

Welcome to the world of RAG and LLM evaluation—you’re already ahead of most beginners!

pgsql
Copy
Edit

---

**That’s all three docs!  
You now have the world’s most beginner-to-expert-friendly RAG-LLM evaluation project docs—ready to copy.**

If you want a PDF/HTML conversion, a quickstart poster, or anything else, just ask!
