"""
GEval Implementation for Correctness Evaluation

This module implements GEval metric for assessing factual correctness
of outputs against expected answers.

Author: Anand Ramkumar
Date: 2025-03-07
"""
from typing import Dict, Any
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
import os
from dotenv import load_dotenv
from pathlib import Path
import openai
import asyncio
import sys
import time

# Add parent directory to Python path to enable imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from rag_query import RagClient
from evaluation_results import EvaluationResults

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Configure OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = os.getenv('OPENAI_MODEL', 'gpt-4')

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Set OpenAI API key globally
openai.api_key = OPENAI_API_KEY

class CorrectnessEvaluator:
    """Evaluator class for assessing factual correctness using GEval."""

    def __init__(self):
        """Initialize the correctness evaluator with GEval metric."""
        self.metric = GEval(
            name="Correctness",
            criteria="Determine whether the actual output is factually correct based on the expected output.",
            evaluation_steps=[
                "Check whether the facts in 'actual output' contradicts any facts in 'expected output'",
                "You should also heavily penalize omission of detail",
                "Vague language, or contradicting OPINIONS, are OK"
            ],
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
                LLMTestCaseParams.EXPECTED_OUTPUT
            ]
        )

    def evaluate(self, input_text: str, actual_output: str, expected_output: str) -> Dict[str, Any]:
        """
        Evaluate the correctness of the actual output against expected output.

        Args:
            input_text (str): The input query or prompt
            actual_output (str): The output to evaluate
            expected_output (str): The ground truth or expected answer

        Returns:
            Dict[str, Any]: Dictionary containing score and reason for the evaluation
        """
        test_case = LLMTestCase(
            input=input_text,
            actual_output=actual_output,
            expected_output=expected_output
        )

        # Run evaluation
        self.metric.measure(test_case)

        return {
            "score": self.metric.score,
            "reason": self.metric.reason
        }

async def main():
    """Run evaluation on test cases using RAG responses."""
    # Initialize evaluator, RAG client, and results handler
    evaluator = CorrectnessEvaluator()
    rag_client = RagClient()
    results_handler = EvaluationResults("D:/RAGOps-Workspace/RAGOps-Suite/ragbench/deep_eval/evaluation_results")
    
    # Load test cases
    json_path = Path(__file__).parent.parent / "synthetic_data" / "20250305_120256.json"
    from test_extractor import TestExtractor
    test_extractor = TestExtractor(str(json_path))
    test_cases = test_extractor.load_test_cases()
    
    # Evaluate each test case
    print(f"\nEvaluating {len(test_cases)} test cases:")
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Input: {test_case.input}")
        print(f"Expected: {test_case.expected_output[:100]}...")
        
        # Get RAG response
        response = await rag_client.query(test_case.input)
        if not response:
            print("Error: Failed to get response from RAG")
            actual_output = ""
            contexts = []
        else:
            actual_output = response['response']
            contexts = response.get('contexts', [])
            print(f"Actual: {actual_output[:1000]}...")
        
        # Evaluate response
        result = evaluator.evaluate(
            input_text=test_case.input,
            actual_output=actual_output,
            expected_output=test_case.expected_output
        )
        
        # Add result to handler
        results_handler.add_result(
            test_case_id=i,
            input_query=test_case.input,
            expected_output=test_case.expected_output,
            actual_output=actual_output,
            score=result['score'],
            reason=result['reason'],
            contexts=contexts
        )
        
        print(f"Score: {result['score']}")
        print(f"Reason: {result['reason']}")
    
    # Save all results
    detailed_file, summary_file = results_handler.save_results()
    print(f"\nResults saved to:")
    print(f"Summary: {summary_file}")
    print(f"Detailed: {detailed_file}")

if __name__ == "__main__":
    asyncio.run(main())