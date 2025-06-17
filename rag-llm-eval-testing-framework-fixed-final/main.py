import os
from typing import List, Dict, Any, Optional
from utils.utils.config_manager import ConfigManager
from utils.utils.data_loader import DataLoader
from utils.utils.scorer import Scorer
from utils.utils.metrics_manager import MetricsManager
from utils.utils.reporter import Reporter
from utils.utils.logger import setup_logger

# Setup a logger for the main application
logger = setup_logger(__name__)

def run_evaluation(
    data_path: str,
    config_path: str,
    output_dir: str,
    model_name: Optional[str] = None,
    metrics: Optional[List[str]] = None,
    report_formats: Optional[List[str]] = None
):
    """
    The main function to run a comprehensive RAG-LLM evaluation.

    This function orchestrates the entire process:
    1. Loads configuration.
    2. Loads the dataset.
    3. Initializes all necessary components (Scorer, MetricsManager, Reporter).
    4. Iterates through the dataset, evaluating each data point.
    5. Generates the final report.

    Args:
        data_path: Path to the evaluation dataset.
        config_path: Path to the configuration JSON file.
        output_dir: Directory where the evaluation report will be saved.
        model_name: (Optional) Override the model name from the config file.
        metrics: (Optional) Override the list of metrics from the config file.
        report_formats: (Optional) Override the report formats from the config file.
    """
    try:
        # 1. Load Configuration
        logger.info(f"Loading configuration from: {config_path}")
        config_manager = ConfigManager(config_path)

        # Override config with CLI arguments if provided
        if model_name:
            config_manager.config['model_name'] = model_name
        if metrics:
            config_manager.config['metrics'] = metrics
        if report_formats:
            config_manager.config.setdefault('reporter', {})['report_formats'] = report_formats

        # 2. Load Data
        logger.info(f"Loading data from: {data_path}")
        dataset = DataLoader.load_data(data_path)

        # 3. Initialize Components
        scorer = Scorer()
        metrics_manager = MetricsManager(scorer, config_manager)
        reporter = Reporter(output_dir=output_dir)

        # 4. Run Evaluation
        logger.info(f"Starting evaluation for {len(dataset)} data points...")
        all_results = []
        for i, data_point in enumerate(dataset):
            logger.info(f"Evaluating data point {i+1}/{len(dataset)}")
            # This is a placeholder for the logic that would get the 'answer'
            # from an LLM call using the 'question' and 'context'.
            # For this refactoring, we assume 'answer' is already in the dataset.
            if "answer" not in data_point:
                 logger.warning(f"Data point {i+1} is missing an 'answer' and will be skipped.")
                 continue

            results = metrics_manager.evaluate_metrics(data_point)
            all_results.extend(results)

        # 5. Generate Report
        logger.info("Evaluation complete. Generating report...")
        final_report_data = [
            {
                "metric": res.__class__.__name__, # Or however you define metric name
                "score": res.score,
                "details": res.details
            } for res in all_results
        ]
        reporter.generate_report(
            final_report_data,
            report_formats=config_manager.get_reporter_config().get("report_formats", ["json", "html"])
        )
        logger.info(f"Report generated successfully in '{output_dir}' directory.")

    except (FileNotFoundError, ValueError) as e:
        logger.error(f"A configuration or data file error occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during evaluation: {e}", exc_info=True)


if __name__ == '__main__':
    # This block allows running main.py directly for default evaluation
    # For command-line usage, rag-eval-cli.py should be used.
    run_evaluation(data_path='data/default_data.csv', config_path='config.json', output_dir='reports')