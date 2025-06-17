import argparse
from main import run_evaluation

def main_cli():
    """
    Command-Line Interface for the RAG-LLM Evaluation Framework.
    
    This script parses command-line arguments and triggers the main
    evaluation function.
    """
    parser = argparse.ArgumentParser(
        description="Run evaluations for RAG-LLM systems.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--data_path",
        type=str,
        required=True,
        help="Path to the evaluation data file (CSV or JSON)."
    )
    
    parser.add_argument(
        "--config_path",
        type=str,
        default="config.json",
        help="Path to the main configuration JSON file."
    )
    
    parser.add_argument(
        "--output_dir",
        type=str,
        default="reports",
        help="Directory to save the evaluation reports."
    )
    
    parser.add_argument(
        "--model_name",
        type=str,
        help="Name of the model to evaluate (overrides config file)."
    )
    
    parser.add_argument(
        "--metrics",
        nargs='+',
        help="A space-separated list of metrics to evaluate (overrides config file)."
    )
    
    parser.add_argument(
        "--report_formats",
        nargs='+',
        default=["json", "html"],
        choices=["json", "html", "pdf"],
        help="A space-separated list of report formats to generate."
    )

    args = parser.parse_args()

    # Call the main evaluation function with the parsed arguments
    run_evaluation(
        data_path=args.data_path,
        config_path=args.config_path,
        output_dir=args.output_dir,
        model_name=args.model_name,
        metrics=args.metrics,
        report_formats=args.report_formats
    )

if __name__ == "__main__":
    main_cli()