"""
Test Case Extractor

Extracts input questions and expected outputs from JSON test cases.
"""

import json
from typing import List, Dict, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class TestCase:
    """Structure for a test case."""
    input: str
    expected_output: str

class TestExtractor:
    """Extracts test cases from JSON files."""
    
    def __init__(self, json_path: str):
        """
        Initialize with path to JSON file.
        
        Args:
            json_path: Path to JSON test cases file
        """
        self.json_path = Path(json_path)
    
    def load_test_cases(self) -> List[TestCase]:
        """
        Load and parse test cases from JSON file.
        
        Returns:
            List of TestCase objects
        """
        with open(self.json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        test_cases = []
        for item in data:
            if 'input' in item and 'expected_output' in item:
                test_case = TestCase(
                    input=item['input'],
                    expected_output=item['expected_output']
                )
                test_cases.append(test_case)
                
        return test_cases

def main():
    """Example usage of test extractor."""
    # Path to your JSON file
    json_path = "D:/RAGOps-Workspace/RAGOps-Suite/ragbench/deep_eval/synthetic_data/20250305_120256.json"
    
    # Create extractor
    extractor = TestExtractor(json_path)
    
    # Load test cases
    test_cases = extractor.load_test_cases()
    
    # Print test cases
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Input: {test_case.input}")
        print(f"Expected Output: {test_case.expected_output[:100]}...")  # Print first 100 chars

if __name__ == "__main__":
    main()