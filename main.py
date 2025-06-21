import argparse
import logging
import sys
from utils.utils.config_manager import ConfigManager
from utils.utils.metrics_manager import MetricsManager
from utils.utils.llm_wrapper import LLMWrapper
from utils.utils.data_loader import DataLoader
from utils.utils.logger import setup_logger
from utils.utils.response_parser import ResponseParser
from utils.utils.scorer import Scorer

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="RAG-LLM Evaluation Testing Framework")
    parser.add_argument('--config', type=str, default="config.json", help="Path to the configuration file")
    parser.add_argument('--model', type=str, required=False, help="Override model name from config")
    parser.add_argument('--metrics', type=str, nargs='+', help="Override metric names from config")
    parser.add_argument('--input', type=str, help="Input file for evaluation (CSV/JSONL)")
    parser.add_argument('--output', type=str, help="Path to save the evaluation results")
    parser.add_argument('--dashboard', action='store_true', help="Launch dashboard UI")
    args = parser.parse_args()

    # Set up logging
    setup_logger()
    logger = logging.getLogger("rag_eval")
    logger.info("Starting RAG-LLM Evaluation Framework")

    # Load configuration
    config = ConfigManager.load(args.config)
    if args.model:
        config["model_name"] = args.model
    if args.metrics:
        config["metrics"] = args.metrics
    if args.input:
        config["input_file"] = args.input
    if args.output:
        config["output_file"] = args.output

    # Handle dashboard launch
    if args.dashboard:
        import subprocess
        logger.info("Launching dashboard UI...")
        subprocess.run(["python", "dashboard/app.py"])
        sys.exit(0)

    # Load test data
    data = DataLoader.load(config["input_file"])

    # Initialize LLM wrapper
    llm = LLMWrapper(model_name=config["model_name"], config=config)

    # Initialize metrics manager
    metrics_manager = MetricsManager(config=config)

    # Initialize response parser
    response_parser = ResponseParser(config=config)

    # Prepare for results
    results = []
    scorer = Scorer(metrics_manager=metrics_manager, response_parser=response_parser, config=config)

    # Evaluate each test case
    for idx, test_case in enumerate(data):
        logger.info(f"Evaluating test case {idx + 1}/{len(data)}")

        # Get model answer if not already present
        if "generated_answer" not in test_case or not test_case["generated_answer"]:
            test_case["generated_answer"] = llm.generate(test_case["query"], context=test_case.get("context_docs"))

        # Parse the model response if needed
        parsed_answer = response_parser.parse(test_case["generated_answer"])

        # Evaluate with all enabled metrics
        metric_scores = scorer.evaluate(test_case, parsed_answer)
        results.append({
            "test_case_id": test_case.get("id", idx),
            "query": test_case["query"],
            "ground_truth_answer": test_case.get("ground_truth_answer"),
            "generated_answer": test_case["generated_answer"],
            "metrics": metric_scores
        })

    # Save or print results
    if "output_file" in config and config["output_file"]:
        DataLoader.save(results, config["output_file"])
        logger.info(f"Results saved to {config['output_file']}")
    else:
        from pprint import pprint
        pprint(results)

if __name__ == "__main__":
    main()
