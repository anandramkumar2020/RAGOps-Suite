"""
Evaluation Results Handler

This module handles the storage and generation of evaluation results in CSV format.

Author: Anand Ramkumar
Date: 2025-03-07
"""

from typing import Dict, Any, List
from pathlib import Path
import csv
from datetime import datetime
import statistics

class EvaluationResults:
    """Class to handle evaluation results and CSV generation."""
    
    def __init__(self, results_dir: str, success_threshold: float = 0.7):
        """
        Initialize the results handler.
        
        Args:
            results_dir (str): Directory to store results
            success_threshold (float): Score threshold for pass/fail (default: 0.7)
        """
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.detailed_results: List[Dict] = []
        self.success_threshold = success_threshold
        
    def add_result(self, test_case_id: int, input_query: str, 
                  expected_output: str, actual_output: str,
                  score: float, reason: str,
                  contexts: List[Dict] = None):
        """Add a single test case result."""
        self.detailed_results.append({
            'Test_Case_ID': test_case_id,
            'Input_Query': input_query,
            'Expected_Output': expected_output,
            'Actual_Output': actual_output,
            'Score': score,
            'Status': 'PASS' if score >= self.success_threshold else 'FAIL',
            'Evaluation_Reason': reason,
            'Context_Files': ';'.join([ctx['file_name'] for ctx in (contexts or [])])
        })
        
    def save_results(self):
        """Save both summary and detailed results to CSV files."""
        # Save detailed results
        detailed_file = self.results_dir / f"detailed_results_{self.timestamp}.csv"
        with open(detailed_file, 'w', newline='', encoding='utf-8') as f:
            if self.detailed_results:
                writer = csv.DictWriter(f, fieldnames=self.detailed_results[0].keys())
                writer.writeheader()
                writer.writerows(self.detailed_results)
        
        # Calculate summary statistics
        scores = [r['Score'] for r in self.detailed_results]
        passed_cases = len([r for r in self.detailed_results if r['Status'] == 'PASS'])
        total_cases = len(self.detailed_results)
        
        summary_data = {
            'Timestamp': self.timestamp,
            'Total_Test_Cases': total_cases,
            'Average_Score': round(statistics.mean(scores) if scores else 0, 2),
            'Success_Rate': round((passed_cases / total_cases * 100) if total_cases else 0, 2),
            'Failed_Queries': len([r for r in self.detailed_results if not r['Actual_Output']]),
            'Passed_Cases': passed_cases,
            'Failed_Cases': total_cases - passed_cases
        }
        
        # Save summary results
        summary_file = self.results_dir / f"summary_results_{self.timestamp}.csv"
        with open(summary_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=summary_data.keys())
            writer.writeheader()
            writer.writerow(summary_data)
            
        return detailed_file, summary_file