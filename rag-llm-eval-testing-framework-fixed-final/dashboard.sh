#!/bin/bash
# This script sets up the necessary environment and launches the Streamlit dashboard.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Verifying System Tools ---"
# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install it to continue."
    exit 1
fi

# Check if Poetry is installed, if not, offer to install it
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not found. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    # Add poetry to the path for the current session
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "--- Setting up Project Environment ---"
# Install dependencies using Poetry if the virtual environment doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment and installing dependencies with Poetry..."
    poetry install
else
    echo "Virtual environment already exists. Skipping installation."
fi

# Create necessary data and log directories
echo "Ensuring data and log directories exist..."
mkdir -p data/results data/datasets logs

# Set environment variables for the application
echo "Exporting environment variables..."
export PYTHONPATH=$PWD
export DB_PATH="data/results/results.db"
export DASHBOARD_THEME="light"

# Launch the dashboard using the poetry environment
echo "--- Starting RAG-LLM Evaluation Dashboard ---"
# Assumes the app is located at dashboard/app.py
poetry run streamlit run dashboard/app.py --server.port 8501 --server.address localhost