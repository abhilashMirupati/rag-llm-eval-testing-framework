import pandas as pd
import json
import os
from main import run_evaluation # Import the main function from our refactored main.py

def setup_example_files():
    """
    Creates temporary data and config files for this example run.
    In a real scenario, these files would already exist.
    """
    print("--- Setting up example data and configuration files ---")
    
    # 1. Create an example dataset as a CSV file
    example_data = [
        {
            "question": "What are the main features of the Eiffel Tower?",
            "answer": "The Eiffel Tower is a wrought-iron lattice tower in Paris, France. It is 324 meters tall and was completed in 1889.",
            "context": "The Eiffel Tower is a wrought-iron lattice tower located on the Champ de Mars in Paris, France. It stands 324 meters tall and was completed in 1889 as the entrance to the 1889 World's Fair.",
            "ground_truth_answer": "The Eiffel Tower is a 324-meter tall wrought-iron lattice tower in Paris, completed in 1889."
        },
        {
            "question": "How does photosynthesis work?",
            "answer": "Photosynthesis is the process by which plants convert light energy into chemical energy to fuel their activities.",
            "context": "Photosynthesis is a process used by plants, algae, and certain bacteria to convert light energy into chemical energy, through a process that uses sunlight, water, and carbon dioxide.",
            "ground_truth_answer": "Photosynthesis converts light energy into chemical energy, using sunlight, water, and CO2."
        }
    ]
    data_path = "example_data.csv"
    pd.DataFrame(example_data).to_csv(data_path, index=False)
    print(f"Created example dataset at: {data_path}")

    # 2. Create an example configuration as a JSON file
    example_config = {
        "model_name": "gpt-4",
        "metrics": [
            "faithfulness",
            "answer_relevance",
            "context_relevance",
            "fluency"
        ],
        "reporter": {
            "report_formats": ["json", "html"]
        }
    }
    config_path = "example_config.json"
    with open(config_path, 'w') as f:
        json.dump(example_config, f, indent=4)
    print(f"Created example configuration at: {config_path}")
    
    return data_path, config_path

def main():
    """
    Main function to run a comprehensive evaluation example.
    This demonstrates the intended usage of the evaluation framework.
    """
    print("\n--- Running Comprehensive Evaluation Example ---")
    
    # Setup the necessary files for the run
    data_path, config_path = setup_example_files()
    output_dir = "example_reports"
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nCalling the main evaluation function...")
    print(f"  - Data: {data_path}")
    print(f"  - Config: {config_path}")
    print(f"  - Output: {output_dir}")
    
    # Call the single, powerful run_evaluation function
    try:
        run_evaluation(
            data_path=data_path,
            config_path=config_path,
            output_dir=output_dir
        )
        print(f"\n--- Example evaluation finished successfully! ---")
        print(f"Check the '{output_dir}' directory for your reports.")
    
    except Exception as e:
        print(f"\n--- An error occurred during the example evaluation ---")
        print(f"Error: {e}")
    
    finally:
        # Clean up the temporary files
        print("\n--- Cleaning up example files ---")
        if os.path.exists(data_path):
            os.remove(data_path)
        if os.path.exists(config_path):
            os.remove(config_path)

if __name__ == "__main__":
    main()