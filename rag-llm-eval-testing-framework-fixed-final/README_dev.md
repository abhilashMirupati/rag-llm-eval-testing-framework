# RAG-LLM Evaluation Framework - Developer Guide

## Project Structure

```
rag-llm-eval/
├── tests/                  # Test files for all metrics
├── utils/                  # Utility functions and helpers
├── models/                 # Model configurations and wrappers
├── dashboard/             # Streamlit dashboard
├── parsers/               # Model-specific response parsers
├── data/                  # Data storage
│   ├── datasets/         # Test datasets
│   └── results/          # Evaluation results
├── logs/                 # Log files
└── config/               # Configuration files
```

## Development Setup

1. Install dependencies:
```bash
poetry install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Run tests:
```bash
poetry run pytest
```

## Adding New Metrics

1. Create a new test file in `tests/`:
```python
# tests/test_new_metric.py
import pytest
from utils.scorer import Scorer

def test_new_metric():
    scorer = Scorer()
    result = scorer.evaluate(
        answer="Sample answer",
        context="Sample context",
        question="Sample question",
        metric_name="new_metric"
    )
    assert 0 <= result.score <= 1
```

2. Add metric implementation in `utils/scorer.py`:
```python
def evaluate_new_metric(self, answer: str, context: str, question: str) -> EvaluationResult:
    # Implement metric logic
    score = calculate_score(answer, context, question)
    return EvaluationResult(
        metric_name="new_metric",
        score=score,
        details={"additional_info": "..."}
    )
```

3. Update configuration in `config.json`:
```json
{
    "evaluation": {
        "metrics": [
            // ... existing metrics ...
            "new_metric"
        ]
    }
}
```

## Adding New Model Support

1. Create a new parser in `parsers/`:
```python
# parsers/new_model_parser.py
from utils.response_parser import ResponseParser

class NewModelParser(ResponseParser):
    @staticmethod
    def parse(response: Any) -> ParsedResponse:
        # Implement parsing logic
        return ParsedResponse(
            text=response.text,
            raw_response=response,
            metadata=response.metadata,
            provider="new_model",
            model=response.model
        )
```

2. Update model configuration in `models/model_config.py`:
```python
def _create_default_config(self):
    default_config = {
        // ... existing models ...
        "new_model": {
            "provider": "new_provider",
            "type": "cloud",
            "model_params": {
                "temperature": 0.7,
                "max_tokens": 2000
            }
        }
    }
```

## Running Tests

1. Run all tests:
```bash
poetry run pytest
```

2. Run specific test file:
```bash
poetry run pytest tests/test_factuality.py
```

3. Run with coverage:
```bash
poetry run pytest --cov=.
```

4. Run with HTML report:
```bash
poetry run pytest --html=report.html
```

## Dashboard Development

1. Start the dashboard:
```bash
./dashboard.sh
```

2. Add new visualizations:
```python
# dashboard/app.py
def plot_new_visualization(df):
    fig = px.scatter(df, x="metric", y="score")
    return fig
```

## CI/CD

1. GitHub Actions workflow:
- Runs on push to main and pull requests
- Daily scheduled runs
- Matrix testing with Python 3.9 and 3.10
- Generates and uploads reports

2. Jenkins pipeline:
- Runs tests and linting
- Generates coverage reports
- Archives artifacts

## Logging

1. Configure logging in your code:
```python
import logging

logger = logging.getLogger(__name__)
logger.info("Operation completed")
logger.error("Error occurred", exc_info=True)
```

2. View logs:
```bash
tail -f logs/evaluation.log
```

## Best Practices

1. Code Style:
- Follow PEP 8
- Use type hints
- Write docstrings
- Keep functions small and focused

2. Testing:
- Write unit tests for all new code
- Use fixtures for common setup
- Test edge cases
- Maintain high coverage

3. Documentation:
- Update README.md for user-facing changes
- Update README_dev.md for developer-facing changes
- Document API changes
- Add examples for new features

4. Version Control:
- Use meaningful commit messages
- Create feature branches
- Keep PRs focused and small
- Review code before merging

## Troubleshooting

1. Common Issues:
- Missing dependencies: Run `poetry install`
- Database errors: Check DB_PATH in .env
- API errors: Verify API keys
- Test failures: Check test data

2. Debugging:
- Use logging for debugging
- Check logs in `logs/`
- Use pytest -v for verbose output
- Use pytest --pdb for interactive debugging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details 