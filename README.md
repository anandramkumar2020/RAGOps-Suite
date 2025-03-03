# RAGOps Suite

A comprehensive suite for RAG (Retrieval Augmented Generation) operations, including implementation and evaluation frameworks.

## Project Structure

- `ragstack/`: Core RAG implementation
  - `backend/`: FastAPI server for RAG operations
  - `frontend/`: React-based user interface
- `ragbench/`: Evaluation framework (coming soon)

## Getting Started

Detailed setup instructions can be found in [environment/setup_instructions.md](environment/setup_instructions.md).

### Quick Start Guide

1. **Start Backend Server**
```bash
# Activate conda environment
conda activate ragstack-env

# Navigate to backend directory
cd ragstack/backend

# Start the server
python main.py

# The backend will be available at http://localhost:8000/docs
# To stop the backend server: Press Ctrl+C in the terminal
```

2. **Start Frontend Development Server**
```bash
# Navigate to frontend directory
cd ragstack/frontend

# Start the development server
npm run dev

# The frontend will be available at http://localhost:5173
# To stop the frontend server: Press Ctrl+C in the terminal
```

### Emergency Stop Procedures (If Terminal Windows Are Lost)

If you've lost access to the original terminal windows and need to stop the servers:

1. **Stop Backend Server**
```bash
# This will stop all Python processes
taskkill /F /IM python.exe
```

2. **Stop Frontend Server**
```bash
# This will stop all Node processes
taskkill /F /IM node.exe
```

Note: These emergency stop commands will terminate all Python and Node.js processes on your system. Use them only when you can't access the original terminals. The preferred method is using Ctrl+C in the respective terminal windows.

## Features

- Simple and intuitive web interface for RAG queries
- FastAPI backend with LlamaIndex integration
- Modern React frontend with Vite
- Easy-to-follow setup and deployment instructions

## RAGBench Evaluation

### Faithfulness Evaluation
The RAGBench evaluation system uses LlamaIndex's FaithfulnessEvaluator to assess if the RAG system's responses are faithful to the source material. 

#### Implementation Details
- Questions are generated using RagDatasetGenerator, which creates QA pairs with reference contexts
- Evaluation uses these reference contexts rather than the contexts returned by the RAG API
- This ensures evaluation against the original source material that generated the questions

#### Important Observations
1. **Context Source**
   - Two potential sources of context for evaluation:
     - Reference contexts from RagDatasetGenerator
     - Contexts returned by RAG API
   - Current implementation uses RagDatasetGenerator contexts for more accurate evaluation

2. **RAG API Context Limitation**
   - The RAG API returns truncated context previews
   - This can lead to false negatives in faithfulness evaluation
   - Example: A correct answer might be marked unfaithful because the supporting evidence is truncated in the API response

3. **Future Considerations**
   - Consider evaluating against both context sources
   - Potential enhancement: Modify RAG API to return full context
   - This would enable evaluation of both answer correctness and retrieval accuracy

## Development

For detailed information about the environment setup and development guidelines, please refer to our [setup instructions](environment/setup_instructions.md).
