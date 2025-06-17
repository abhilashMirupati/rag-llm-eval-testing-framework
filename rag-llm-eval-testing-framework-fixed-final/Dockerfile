# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY . .

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Create necessary directories
RUN mkdir -p data/results data/datasets logs

# Set environment variables
ENV PYTHONPATH=/app
ENV DB_PATH=/app/data/results/results.db
ENV DASHBOARD_THEME=light
ENV DASHBOARD_PORT=8501
ENV DASHBOARD_HOST=0.0.0.0

# Expose port
EXPOSE 8501

# Run the dashboard
CMD ["streamlit", "run", "dashboard/app.py"] 