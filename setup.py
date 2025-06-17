from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the contents of your requirements file
with open("requirements.txt", "r", encoding="utf-8") as fh:
    # Filter out comments and empty lines
    requirements = [line.strip() for line in fh if line.strip() and not line.strip().startswith('#')]

setup(
    name="rag-llm-eval",
    version="0.2.0", # Incremented version for new release
    # TODO: Update with your name and email
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive framework for evaluating RAG systems with LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # TODO: Update with your actual project URL
    url="https://github.com/yourusername/rag-llm-eval",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            # CRITICAL FIX: This now correctly points to the main_cli function
            # in your refactored rag-eval-cli.py script.
            "rag-eval=rag_eval_cli:main_cli",
        ],
    },
)