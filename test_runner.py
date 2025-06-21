import logging
from utils.utils.config_manager import ConfigManager
from utils.utils.metrics_manager import MetricsManager
from utils.utils.llm_wrapper import LLMWrapper
from utils.utils.data_loader import DataLoader
from utils.utils.logger import setup_logger
from utils.utils.response_parser import ResponseParser
from utils.utils.scorer import Scorer

def run_tests(config_path="config.json", input_file=None, output_file=None, model=None, metrics=None):
    setup_logger()
    logger = logging.getLogger("test_runner")
    logger.info("Starting RAG-LLM Evaluation Test Runner")

    config = ConfigManager.load(config_path)
    if model:
        config["model_name"] = model
    if metrics:
        config["metrics"] = metrics
    if input_file:
        config["input_file"] = input_file
    if output_file:
        config["output_file"] = output_file

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
    run_tests()
