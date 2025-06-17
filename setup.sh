#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Setting up Python virtual environment ---"
# Check if python3 is available
if ! command -v python3 &> /dev/null
then
    echo "Error: python3 could not be found. Please install Python 3.9 or higher."
    exit 1
fi

# Create a virtual environment in the .venv directory
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

echo "--- Installing dependencies from requirements.txt ---"
# Upgrade pip and install all requirements
pip install --upgrade pip
pip install -r requirements.txt

echo "--- Downloading spaCy model ---"
# Download the required English model for spaCy
python -m spacy download en_core_web_sm

echo "--- Setup complete! ---"
echo "To activate the environment, run: source .venv/bin/activate"