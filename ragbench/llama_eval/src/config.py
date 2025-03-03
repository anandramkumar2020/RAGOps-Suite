"""Configuration constants for the RAGOps evaluation framework."""

class Config:
    # OpenAI Settings
    OPENAI_MODEL = "gpt-3.5-turbo"
    TEMPERATURE = 0.3
    
    # RAG API Settings
    API_ENDPOINT = "http://localhost:8000"
    API_QUERY_PATH = "/api/query"
    
    # Evaluation Settings
    WORKERS = 8
    THRESHOLDS = {
        "faithfulness": 1.0,
        "relevancy": 0.7,
        "context_relevancy": 0.7
    }
    RESULTS_DIR = "evaluation_results"
    
    # QA Generation Settings
    CHUNK_SIZE = 512  # Number of tokens per chunk
    QUESTIONS_PER_CHUNK = 4
    
    # Input/Output Settings
    DOCUMENTS_DIR = "./data/test_documents"
    QA_OUTPUT_FILE = "generated_qa_pairs.json"
    QUESTIONS_OUTPUT_FILE = "generated_questions.txt"
