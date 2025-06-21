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
    parser = argparse.ArgumentParser(description="RAG-LLM Evaluation CLI")
    parser.add_argument('--config', type=str, default="config.json", help="Configuration file path")
    parser.add_argument('--input', type=str, help="Input file (CSV/JSONL)")
    parser.add_argument('--output', type=str, help="Output file for results")
    parser.add_argument('--model', type=str, help="Model override")
    parser.add_argument('--metrics', type=str, nargs='+', help="Metrics override")
    parser.add_argument('--dashboard', action='store_true', help="Launch dashboard UI")
    args = parser.parse_args()

    setup_logger()
    logger = logging.getLogger("rag_eval_cli")
    logger.info("Launching RAG-LLM Evaluation CLI")

    config = ConfigManager.load(args.config)
    if args.model:
        config["model_name"] = args.model
    if args.metrics:
        config["metrics"] = args.metrics
    if args.input:
        config["input_file"] = args.input
    if args.output:
        config["output_file"] = args.output

    if args.dashboard:
        import subprocess
        logger.info("Launching dashboard UI via CLI...")
        subprocess.run(["python", "dashboard/app.py"])
        sys.exit(0)

    data = DataLoader.load(config["input_file"])
    llm = LLMWrapper(model_name=config["model_name"], config=config)
    metrics_manager = MetricsManager(config=config)
    response_parser = ResponseParser(config=config)
    scorer = Scorer(metrics_manager=metrics_manager, response_parser=response_parser, config=config)

    results = []
    for idx, test_case in enumerate(data):
        logger.info(f"Evaluating test case {idx + 1}/{len(data)}")
        if "generated_answer" not in test_case or not test_case["generated_answer"]:
            test_case["generated_answer"] = llm.generate(test_case["query"], context=test_case.get("context_docs"))
        parsed_answer = response_parser.parse(test_case["generated_answer"])
        metric_scores = scorer.evaluate(test_case, parsed_answer)
        results.append({
            "test_case_id": test_case.get("id", idx),
            "query": test_case["query"],
            "ground_truth_answer": test_case.get("ground_truth_answer"),
            "generated_answer": test_case["generated_answer"],
            "metrics": metric_scores
        })

    if "output_file" in config and config["output_file"]:
        DataLoader.save(results, config["output_file"])
        logger.info(f"Results saved to {config['output_file']}")
    else:
        from pprint import pprint
        pprint(results)

if __name__ == "__main__":
    main()
