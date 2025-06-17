# Guide for Freshers

Welcome to the RAG LLM Evaluation Framework! This guide will help you get started with the project.

## Quick Start

1. **Setup Environment**:
```bash
# Clone the repository
git clone https://github.com/yourusername/rag-llm-eval-testing-framework.git
cd rag-llm-eval-testing-framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

2. **Configure LLM**:
Edit `config.json` to set up your preferred LLM:
```json
{
    "models": [
        {
            "name": "gpt-4",
            "enabled": true,
            "parameters": {
                "temperature": 0.7
            }
        }
    ]
}
```

3. **Run Tests**:
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_framework.py

# Run with coverage report
python -m pytest --cov=utils tests/
```

4. **Start Dashboard**:
```bash
# Start the dashboard
./dashboard.sh
# Or
python dashboard/app.py
```

## Project Structure

```
rag-llm-eval-testing-framework/
├── utils/                    # Core utilities
│   └── utils/
│       ├── data_loader.py    # Data loading utilities
│       ├── config_manager.py # Configuration management
│       ├── metrics_manager.py# Metric calculations
│       ├── report_generator.py# Report generation
│       ├── logger.py        # Logging utilities
│       └── templates/       # HTML templates
├── tests/                   # Test files
├── examples/               # Example implementations
├── dashboard/             # Dashboard application
├── models/               # Model implementations
├── config.json          # Configuration file
├── requirements.txt     # Dependencies
└── README.md           # Project documentation
```

## Key Files to Know

1. **Configuration**:
   - `config.json`: Main configuration file
   - `utils/utils/config_manager.py`: Configuration management

2. **Testing**:
   - `tests/test_framework.py`: Main test suite
   - `test_runner.py`: Test runner script

3. **Dashboard**:
   - `dashboard/app.py`: Dashboard application
   - `dashboard.sh`: Dashboard startup script

4. **Examples**:
   - `examples/basic_usage.py`: Basic usage examples
   - `examples/advanced_usage.py`: Advanced usage examples

## Common Tasks

### 1. Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_framework.py -v

# Run with coverage
python -m pytest --cov=utils tests/
```

### 2. Starting Dashboard
```bash
# Using script
./dashboard.sh

# Using Python
python dashboard/app.py
```

### 3. Adding New Metrics
1. Add metric implementation in `utils/utils/metrics_manager.py`
2. Update configuration in `config.json`
3. Add tests in `tests/test_framework.py`

### 4. Generating Reports
```python
from utils.utils.report_generator import ReportGenerator

generator = ReportGenerator()
report_path = generator.generate_report(
    results,
    metadata={"model": "gpt-4"},
    format="html"
)
```

## Troubleshooting

1. **Dashboard Not Starting**:
   - Check if port 8501 is available
   - Verify all dependencies are installed
   - Check dashboard logs

2. **Tests Failing**:
   - Check test data in `tests/test_data/`
   - Verify configuration in `config.json`
   - Check test logs

3. **LLM Connection Issues**:
   - Verify API keys in configuration
   - Check network connection
   - Verify model availability

## Learning Resources

1. **Documentation**:
   - README.md: Project overview
   - CONTRIBUTING.md: Contribution guidelines
   - CODE_OF_CONDUCT.md: Code of conduct

2. **Examples**:
   - `examples/basic_usage.py`: Basic examples
   - `examples/advanced_usage.py`: Advanced examples

3. **Tests**:
   - `tests/test_framework.py`: Test examples
   - `tests/test_data/`: Test data examples

## Getting Help

1. Check existing issues on GitHub
2. Create a new issue for bugs
3. Ask questions in discussions
4. Contact maintainers

## Next Steps

1. Read the README.md
2. Try the examples
3. Run the tests
4. Start the dashboard
5. Make your first contribution

Remember: Don't hesitate to ask questions and explore the codebase! 