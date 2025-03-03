# RAGOps Evaluation Framework

A comprehensive evaluation framework for RAG (Retrieval Augmented Generation) applications, providing tools for measuring and improving RAG system performance.

## Features

- **Multiple Evaluation Metrics**:
  - Faithfulness Evaluation: Measures if the response is consistent with provided context
  - Answer Relevancy: Evaluates if the response answers the query
  - Context Relevancy: Assesses if retrieved contexts are relevant to the query
  - *(Coming Soon)* Correctness Evaluation: Compares against ground truth
  - *(Coming Soon)* Semantic Similarity: Measures semantic closeness to reference answers
  - *(Coming Soon)* Guideline Adherence: Checks compliance with specified guidelines

- **Batch Processing**:
  - Asynchronous evaluation of multiple queries
  - Detailed per-query metrics
  - Aggregated performance statistics
  - Parallel processing with configurable workers

- **Comprehensive Reporting**:
  - CSV exports for detailed analysis
  - Summary statistics
  - Performance tracking over time
  - Detailed feedback for each evaluation metric

## Project Structure

```
ragbench/
├── llama_eval/           # Core evaluation framework
│   ├── src/
│   │   ├── batch_evaluator.py    # Batch evaluation implementation
│   │   ├── qa_generator.py       # Test case generation
│   │   └── README.md            # Framework documentation
│   └── examples/               # Example test cases
│       └── generated_qa_pairs.json
├── docs/                # Documentation
│   ├── metrics.md      # Detailed metrics documentation
│   └── api.md          # API documentation
└── tests/              # Framework tests
```

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/RAGOps-Suite.git
cd RAGOps-Suite

# Create and activate conda environment
conda env create -f environment/environment.yml
conda activate ragops-eval

# Set up environment variables
cp ragbench/llama_eval/.env.example ragbench/llama_eval/.env
# Add your OpenAI API key to .env
```

### Basic Usage

```python
from ragbench.llama_eval.src.batch_evaluator import BatchRagEvaluator

# Initialize evaluator
evaluator = BatchRagEvaluator(api_endpoint="your_rag_api_endpoint")

# Load test cases
qa_pairs = evaluator.load_qa_pairs("path/to/qa_pairs.json")

# Run evaluation
await evaluator.evaluate_all()
```

### Example Output

```python
Evaluation Summary:
Total Queries: 100
Average Faithfulness Score: 0.85
Average Answer Relevancy Score: 0.92
Average Context Relevancy Score: 0.88
Passing Faithfulness: 85
Passing Answer Relevancy: 92
Passing Context Relevancy: 88
```

## Example RAG Implementation

Check out the `examples/ragstack` directory for a sample RAG implementation that demonstrates:
- FastAPI-based RAG service
- React frontend for testing
- Integration with the evaluation framework

## Documentation

- [API Documentation](docs/api.md)
- [Metrics Documentation](docs/metrics.md)
- [Environment Setup](environment/setup_instructions.md)
- [Example RAG Implementation](examples/ragstack/README.md)

## Contributing

We welcome contributions! Please check our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
