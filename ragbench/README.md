# RAGBench - RAG Evaluation Suite

A comprehensive evaluation framework for RAG systems using multiple evaluation tools.

## Evaluation Tools

- `llama_eval/` - LlamaIndex-based evaluation tools
- `deep_eval/` - DeepEval framework implementation
- `giskard_eval/` - Giskard evaluation suite

## Environment Setup

```bash
# Create conda environment
conda create -n ragbench-env python=3.10 -y
conda activate ragbench-env

# Install dependencies
pip install -r requirements.txt
```

## Directory Structure
```
ragbench/
├── requirements.txt      # Unified dependencies
├── llama_eval/          # LlamaIndex evaluation
├── deep_eval/           # DeepEval framework
└── giskard_eval/        # Giskard evaluation
```

## Usage

Each evaluation tool can be used independently but shares the same environment:

1. LlamaIndex Evaluation:
   ```bash
   cd llama_eval
   python src/generate_dataset.py
   ```

2. DeepEval Framework:
   ```bash
   cd deep_eval
   # commands will be added
   ```

3. Giskard Evaluation:
   ```bash
   cd giskard_eval
   # commands will be added
   ```

## Common Utilities

All evaluation tools share common utilities for:
- Metrics calculation
- Result visualization
- Report generation

## Environment Management

- Single conda environment (`ragbench-env`) for all tools
- Centralized dependency management
- Consistent versioning across tools
