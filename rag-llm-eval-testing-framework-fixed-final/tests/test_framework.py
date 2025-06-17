import pytest

def test_import_core_components():
    """
    Tests that all major components of the framework can be imported without error.
    This is a basic sanity check to ensure the project structure is intact.
    """
    try:
        from utils.utils.scorer import Scorer
        from utils.utils.reporter import Reporter
        from utils.utils.metrics_manager import MetricsManager
        from utils.utils.config_manager import ConfigManager
        from main import run_evaluation
    except ImportError as e:
        pytest.fail(f"Failed to import a core component: {e}")

def test_scorer_has_all_evaluation_methods():
    """
    Verifies that the Scorer class has all the required 'evaluate_*' methods.
    This test protects against accidental deletion or renaming of metric methods.
    """
    from utils.utils.scorer import Scorer
    scorer_instance = Scorer()
    
    expected_methods = [
        "evaluate_answer_relevance",
        "evaluate_context_relevance",
        "evaluate_context_precision",
        "evaluate_context_recall",
        "evaluate_faithfulness",
        "evaluate_factuality",
        "evaluate_hallucination",
        "evaluate_coherence",
        "evaluate_completeness",
        "evaluate_conciseness",
        "evaluate_answer_similarity",
        "evaluate_fluency",
        "evaluate_groundedness",
        "evaluate_redundancy",
        "evaluate_instruction_following",
        "evaluate_overall_quality"
    ]
    
    missing_methods = []
    for method_name in expected_methods:
        if not hasattr(scorer_instance, method_name):
            missing_methods.append(method_name)
            
    assert not missing_methods, \
        f"The Scorer is missing the following required methods: {', '.join(missing_methods)}"

def test_default_configurations_load():
    """
    Tests that the default configuration files can be loaded without errors.
    """
    try:
        # Test loading the main config.json
        from utils.utils.config_manager import ConfigManager
        ConfigManager() # This will load the default 'config.json'
        
        # Test loading the metric/model capabilities
        from models.models.metric_config import metric_manager
        assert metric_manager.get_metric("faithfulness") is not None, "Failed to load from model_capabilities.yaml"

    except Exception as e:
        pytest.fail(f"Failed to load a default configuration file: {e}")