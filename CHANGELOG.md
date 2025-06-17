# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-05-15

### Added
- **Enhanced Scorer**: Implemented a full suite of 16+ evaluation metrics in `utils/scorer.py`, including `factuality`, `completeness`, `hallucination`, `answer_similarity`, and more, using robust libraries like `deepeval` and `spacy`.
- **Centralized Reporting**: Created a dedicated `utils/reporter.py` to handle JSON, HTML, and PDF report generation, using Jinja2 for templating.
- **Robust CLI**: Improved `rag-eval-cli.py` with more descriptive help messages and validation for arguments.
- **Advanced Dashboard**: Optimized `dashboard/app.py` with Streamlit caching (`@st.cache_data`) for performance, enhanced UI components, and integrated PDF reporting.
- **Comprehensive Testing**: Expanded the test suite in `tests/` with a `BaseMetricTest` class to standardize metric testing, added new integration tests, and ensured all components are validated.
- **Singleton Configuration Managers**: Implemented `MetricManager` and `ModelManager` as singletons to ensure a consistent, single source of truth for configurations across the framework.
- **Developer Documentation**: Significantly improved `README_dev.md` with detailed guides for adding new metrics and models.
- **Setup Scripts**: Enhanced `setup.sh` and `dashboard.sh` with better error checking and user feedback.

### Changed
- **Refactored `main.py`**: Streamlined the main evaluation flow for better readability and orchestration of components.
- **Optimized `DataLoader`**: Improved error handling and validation for data loading from CSV and JSON files.
- **Standardized Project Structure**: Re-organized files and directories for better logical grouping and clarity, as reflected in documentation.

### Fixed
- **`setup.py` Entry Point**: Corrected the `console_scripts` entry point to correctly point to the CLI function.
- **Dependency Management**: Cleaned up `requirements.txt` and ensured all necessary packages for the enhanced features are included.

## [0.1.0] - 2024-03-20

### Added
- Project initialization with a basic directory structure.
- Initial implementation of core evaluation metrics.
- First version of the Streamlit dashboard for visualization.
- Basic support for major LLM providers.
- Initial documentation, including `README.md` and `CONTRIBUTING.md`.
