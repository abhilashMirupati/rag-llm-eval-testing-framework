"""
Test runner for RAG-LLM evaluation framework with automatic test discovery and retry functionality.
"""

import os
import sys
import pytest
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import json
import sqlite3
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.getenv("LOG_FILE", "logs/evaluation.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TestRunner:
    """Test runner for RAG-LLM evaluation framework."""
    
    def __init__(self):
        """Initialize test runner."""
        self.db_path = os.getenv("DB_PATH", "data/results.db")
        self.test_batch_size = int(os.getenv("TEST_BATCH_SIZE", "10"))
        self.test_max_retries = int(os.getenv("TEST_MAX_RETRIES", "3"))
        self.test_timeout = int(os.getenv("TEST_TIMEOUT", "30"))
        self.metrics_to_run = os.getenv("METRICS_TO_RUN", "").split(",")
        
        # Ensure database directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Initialize database
        self._init_db()
    
    def _init_db(self):
        """Initialize SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create results table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            model_name TEXT,
            dataset_name TEXT,
            metric_name TEXT,
            score REAL,
            details TEXT,
            status TEXT,
            error_message TEXT
        )
        """)
        
        conn.commit()
        conn.close()
    
    def discover_tests(self) -> List[str]:
        """Discover all test files in the tests directory."""
        test_dir = Path("tests")
        test_files = []
        
        for file in test_dir.glob("test_*.py"):
            if file.name != "test_runner.py":
                test_files.append(str(file))
        
        return test_files
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def run_test(self, test_file: str) -> Dict[str, Any]:
        """Run a single test file with retry functionality."""
        try:
            # Run pytest on the test file
            result = pytest.main([
                test_file,
                "-v",
                "--tb=short",
                f"--timeout={self.test_timeout}"
            ])
            
            # Extract metric name from test file
            metric_name = Path(test_file).stem.replace("test_", "")
            
            # Get test results
            test_results = self._get_test_results(test_file)
            
            return {
                "metric_name": metric_name,
                "status": "passed" if result == 0 else "failed",
                "results": test_results
            }
        
        except Exception as e:
            logger.error(f"Error running test {test_file}: {str(e)}")
            return {
                "metric_name": Path(test_file).stem.replace("test_", ""),
                "status": "error",
                "error_message": str(e)
            }
    
    def _get_test_results(self, test_file: str) -> List[Dict[str, Any]]:
        """Extract results from test file execution."""
        # This is a placeholder - in a real implementation, you would
        # parse the test output or use pytest's result collection
        return []
    
    def save_results(self, results: Dict[str, Any]):
        """Save test results to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO results (
            model_name,
            dataset_name,
            metric_name,
            score,
            details,
            status,
            error_message
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            results.get("model_name", "default"),
            results.get("dataset_name", "default"),
            results["metric_name"],
            results.get("score", 0.0),
            json.dumps(results.get("results", [])),
            results["status"],
            results.get("error_message", "")
        ))
        
        conn.commit()
        conn.close()
    
    def run_all_tests(self):
        """Run all discovered tests."""
        test_files = self.discover_tests()
        logger.info(f"Discovered {len(test_files)} test files")
        
        for test_file in test_files:
            logger.info(f"Running test: {test_file}")
            results = self.run_test(test_file)
            self.save_results(results)
            
            if results["status"] == "passed":
                logger.info(f"Test passed: {test_file}")
            else:
                logger.warning(f"Test failed: {test_file}")
    
    def run_specific_metrics(self, metrics: List[str]):
        """Run tests for specific metrics."""
        test_files = self.discover_tests()
        metrics_to_run = [f"test_{metric}.py" for metric in metrics]
        
        for test_file in test_files:
            if Path(test_file).name in metrics_to_run:
                logger.info(f"Running test: {test_file}")
                results = self.run_test(test_file)
                self.save_results(results)
    
    def get_results_summary(self) -> Dict[str, Any]:
        """Get summary of test results."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get overall statistics
        cursor.execute("""
        SELECT 
            COUNT(*) as total_tests,
            SUM(CASE WHEN status = 'passed' THEN 1 ELSE 0 END) as passed_tests,
            AVG(score) as average_score
        FROM results
        WHERE timestamp >= datetime('now', '-1 day')
        """)
        
        stats = cursor.fetchone()
        
        # Get metric-wise statistics
        cursor.execute("""
        SELECT 
            metric_name,
            COUNT(*) as total,
            AVG(score) as average_score,
            MIN(score) as min_score,
            MAX(score) as max_score
        FROM results
        WHERE timestamp >= datetime('now', '-1 day')
        GROUP BY metric_name
        """)
        
        metric_stats = cursor.fetchall()
        
        conn.close()
        
        return {
            "total_tests": stats[0],
            "passed_tests": stats[1],
            "average_score": stats[2],
            "metric_stats": {
                metric: {
                    "total": total,
                    "average_score": avg_score,
                    "min_score": min_score,
                    "max_score": max_score
                }
                for metric, total, avg_score, min_score, max_score in metric_stats
            }
        }

def main():
    """Main entry point for test runner."""
    runner = TestRunner()
    
    if len(sys.argv) > 1:
        # Run specific metrics
        metrics = sys.argv[1:]
        runner.run_specific_metrics(metrics)
    else:
        # Run all tests
        runner.run_all_tests()
    
    # Print results summary
    summary = runner.get_results_summary()
    logger.info("Test Results Summary:")
    logger.info(f"Total Tests: {summary['total_tests']}")
    logger.info(f"Passed Tests: {summary['passed_tests']}")
    logger.info(f"Average Score: {summary['average_score']:.2f}")
    
    logger.info("\nMetric-wise Statistics:")
    for metric, stats in summary["metric_stats"].items():
        logger.info(f"\n{metric}:")
        logger.info(f"  Total Tests: {stats['total']}")
        logger.info(f"  Average Score: {stats['average_score']:.2f}")
        logger.info(f"  Min Score: {stats['min_score']:.2f}")
        logger.info(f"  Max Score: {stats['max_score']:.2f}")

if __name__ == "__main__":
    main() 