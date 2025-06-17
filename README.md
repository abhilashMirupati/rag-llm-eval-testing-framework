# RAG LLM Evaluation Framework

A comprehensive framework for evaluating Retrieval-Augmented Generation (RAG) systems with various LLMs.

## Features

- Multiple evaluation metrics
- Support for various LLMs
- Interactive dashboard
- Comprehensive reporting
- Easy configuration
- Extensive test suite

## LLM Compatibility

| LLM Model | Supported Metrics | Notes |
|-----------|------------------|--------|
| GPT-4 | All metrics | Best performance, recommended for production |
| GPT-3.5 | All metrics | Good balance of performance and cost |
| Claude | All metrics | Strong performance, good for long-form content |
| Llama 2 | Basic metrics | Open source, good for testing |
| Mistral | Basic metrics | Open source, efficient performance |

### Metric Support Details

| Metric | GPT-4 | GPT-3.5 | Claude | Llama 2 | Mistral |
|--------|-------|---------|--------|---------|---------|
| Factuality | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |
| Context Precision | ✅ | ✅ | ✅ | ✅ | ✅ |
| Context Recall | ✅ | ✅ | ✅ | ✅ | ✅ |
| Faithfulness | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |
| Hallucination | ✅ | ✅ | ✅ | ❌ | ❌ |
| QA Match | ✅ | ✅ | ✅ | ✅ | ✅ |
| Helpfulness | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |
| Coherence | ✅ | ✅ | ✅ | ✅ | ✅ |
| Conciseness | ✅ | ✅ | ✅ | ✅ | ✅ |
| Completeness | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |

Legend:
- ✅: Fully supported
- ⚠️: Partial support
- ❌: Not supported

## Quick Start

1. **Installation**:
```bash
pip install -r requirements.txt
```

2. **Configuration**:
Edit `config.json` to set up your preferred LLM and metrics.

3. **Run Tests**:
```bash
python -m pytest tests/
```

4. **Start Dashboard**:
```bash
./dashboard.sh
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

## Documentation

- [Guide for Freshers](GUIDE_FOR_FRESHERS.md): Comprehensive guide for newcomers
- [Contributing Guidelines](CONTRIBUTING.md): How to contribute to the project
- [Code of Conduct](CODE_OF_CONDUCT.md): Community guidelines

## Key Components

### 1. Metrics Manager
- Handles metric calculations
- Supports multiple evaluation metrics
- Provides aggregation functions

### 2. Data Loader
- Supports multiple input formats (JSON, CSV, YAML, XML, TXT)
- Data validation and preprocessing
- Flexible data structure

### 3. Report Generator
- Generates comprehensive reports
- Supports multiple formats (HTML, JSON, CSV)
- Includes visualizations

### 4. Dashboard
- Interactive visualization
- Real-time monitoring
- Customizable views

## Usage Examples

### Basic Usage
```python
from utils.utils.metrics_manager import MetricsManager
from utils.utils.data_loader import DataLoader

# Load data
data = DataLoader.load_json("data.json")

# Calculate metrics
metrics = MetricsManager()
results = metrics.calculate_all_metrics(data)
```

### Advanced Usage
```python
from utils.utils.report_generator import ReportGenerator
from utils.utils.config_manager import ConfigManager

# Load configuration
config = ConfigManager.load_config("config.json")

# Generate report
generator = ReportGenerator()
report = generator.generate_report(
    results,
    metadata={"model": "gpt-4"},
    format="html"
)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Create an issue for bugs
- Ask questions in discussions
- Contact maintainers

## Acknowledgments

- Contributors
- Open source community
- Research papers and resources 