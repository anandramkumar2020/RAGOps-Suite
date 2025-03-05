class Config:
    """Configuration settings for DeepEval implementation."""
    
    # Model settings
    MODEL_NAME = "gpt-4o-mini"
    
    # File paths
    DOCS_FOLDER = "D:/RAGOps-Workspace/RAGOps-Suite/ragbench/deep_eval/data/test_documents"
    OUTPUT_DIR = "./synthetic_data"
    
    # File settings
    SUPPORTED_EXTENSIONS = ['.txt', '.pdf', '.md']
    OUTPUT_FORMAT = 'json'
    
    # Generation settings
    INCLUDE_EXPECTED_OUTPUT = True
