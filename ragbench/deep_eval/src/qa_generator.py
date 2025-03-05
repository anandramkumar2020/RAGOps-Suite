import os
import json
from dotenv import load_dotenv
from deepeval.synthesizer import Synthesizer

"""
QA Generator module for generating question-answer pairs.

This module provides functionality to generate question-answer pairs
from given input text or documents.
"""

class QAGenerator:
    def __init__(self):
        """Initialize the QA Generator."""
        pass

    def generate_qa_pairs(self, text):
        """
        Generate question-answer pairs from the input text.

        Args:
            text (str): Input text to generate QA pairs from

        Returns:
            list: List of dictionaries containing question-answer pairs
        """
        # TODO: Implement QA generation logic

        print("I am Starting")
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        


        synthesizer = Synthesizer(
            model="gpt-4o-mini"
        )

        synthesizer.generate_goldens_from_docs(
            document_paths=['D:/RAGOps-Workspace/RAGOps-Suite/ragbench/deep_eval/data/test_documents/paul.pdf'],
            include_expected_output=True
        )


        synthesizer.save_as(
            # Or 'csv'
            file_type='json',
            directory="./synthetic_data"
        )
        print("I am done")

if __name__ == "__main__":
    # Example usage
    generator = QAGenerator()
    sample_text = "Sample text for QA generation."
    qa_pairs = generator.generate_qa_pairs(sample_text)
