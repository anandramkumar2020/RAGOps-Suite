"""
QA Generator module for generating question-answer pairs using DeepEval Synthesizer.

This module provides functionality to generate question-answer pairs
from documents using the DeepEval framework.
"""

import os
import json
import logging
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from deepeval.synthesizer import Synthesizer
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class QAGenerator:
    """A class for generating question-answer pairs using DeepEval Synthesizer."""
    
    def __init__(self, model: str = Config.MODEL_NAME):
        """
        Initialize the QA Generator.
        
        Args:
            model: The model to use for generation (default from Config.MODEL_NAME)
        """
        self._init_environment()
        self.model = model
        self.synthesizer = None
        
    def _init_environment(self) -> None:
        """Initialize environment variables and validate API key."""
        try:
            load_dotenv()
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API key not found in environment variables")
        except Exception as e:
            logger.error(f"Error initializing environment: {str(e)}")
            raise

    def _init_synthesizer(self) -> None:
        """Initialize the DeepEval Synthesizer."""
        try:
            if not self.synthesizer:
                self.synthesizer = Synthesizer(model=self.model)
                logger.info(f"Initialized Synthesizer with model: {self.model}")
        except Exception as e:
            logger.error(f"Error initializing synthesizer: {str(e)}")
            raise

    def generate_qa_pairs(self, document_paths: List[str]) -> Dict[str, Any]:
        """
        Generate question-answer pairs from documents.

        Args:
            document_paths: List of document paths to generate QA pairs from

        Returns:
            Dict containing status and output path
        """
        try:
            logger.info("Starting QA pair generation")
            
            # Initialize synthesizer if not already initialized
            self._init_synthesizer()
            
            # Generate goldens
            self.synthesizer.generate_goldens_from_docs(
                document_paths=document_paths,
                include_expected_output=Config.INCLUDE_EXPECTED_OUTPUT
            )
            logger.info("Generated golden QA pairs")
            
            # Save results
            output_path = self.synthesizer.save_as(
                file_type=Config.OUTPUT_FORMAT,
                directory=Config.OUTPUT_DIR
            )
            logger.info(f"Saved QA pairs to {output_path}")
            
            return {
                "status": "success",
                "output_path": output_path
            }
            
        except Exception as e:
            logger.error(f"Error in QA pair generation: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

def get_document_paths(folder_path: str) -> List[str]:
    """Get all document paths from a folder."""
    folder = Path(folder_path)
    if not folder.exists():
        raise ValueError(f"Folder not found: {folder_path}")
    
    # Get all files with supported extensions
    document_paths = []
    
    for ext in Config.SUPPORTED_EXTENSIONS:
        document_paths.extend([str(f) for f in folder.glob(f"**/*{ext}")])
    
    logger.info(f"Found {len(document_paths)} documents in {folder_path}")
    return document_paths

def main():
    """Example usage of QA Generator."""
    try:
        # Initialize generator
        generator = QAGenerator()
        
        # Get all documents from the folder
        document_paths = get_document_paths(Config.DOCS_FOLDER)
        
        # Generate QA pairs from all documents
        result = generator.generate_qa_pairs(document_paths)
        
        # Print result
        if result["status"] == "success":
            logger.info(f"Successfully generated QA pairs. Output saved to: {result['output_path']}")
        else:
            logger.error(f"Error generating QA pairs: {result['error']}")
            
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()