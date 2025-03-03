from typing import List, Any, Dict
from pathlib import Path
from llama_index.core import SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI
from llama_index.core.llama_dataset.generator import RagDatasetGenerator
import os
import json
from dotenv import load_dotenv

class QAGenerator:
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.3):
        """Initialize QA Generator.
        
        Args:
            model_name: Name of the OpenAI model to use
            temperature: Temperature for generation (0.3 = balanced between focused and creative)
        """
        self._init_openai()
        self.llm = OpenAI(model=model_name, temperature=temperature)
        
    def _init_openai(self) -> None:
        """Initialize OpenAI credentials."""
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
            
    def load_documents(self, docs_dir: str) -> List[Any]:
        """Load documents from directory.
        
        Args:
            docs_dir: Path to documents directory
            
        Returns:
            List of loaded documents
        """
        if not Path(docs_dir).exists():
            raise FileNotFoundError(f"Directory not found: {docs_dir}")
            
        reader = SimpleDirectoryReader(docs_dir)
        documents = reader.load_data()
        print(f"Found documents: {[doc.metadata['file_name'] for doc in documents]}")
        return documents
        
    def generate_questions(self, documents: List[Any], questions_per_chunk: int = 2) -> List[Dict[str, Any]]:
        """Generate questions from documents using LlamaIndex's RagDatasetGenerator.
        
        Args:
            documents: List of documents to generate questions from
            questions_per_chunk: Number of questions to generate per document chunk
            
        Returns:
            List of dictionaries containing questions, answers, and context
        """
        print("Initializing dataset generator...")
        data_generator = RagDatasetGenerator.from_documents(
            documents,
            llm=self.llm,
            num_questions_per_chunk=questions_per_chunk,
            show_progress=True
        )
        
        print("Generating questions...")
        # Generate questions from all documents at once
        dataset = data_generator.generate_questions_from_nodes()
        
        # Extract questions, answers, and context from the dataset
        qa_pairs = []
        for example in dataset.examples:
            qa_pair = {
                'query': example.query,
                'query_by': str(example.query_by) if example.query_by else "unknown",
                'reference_answer': example.reference_answer,
                'reference_answer_by': str(example.reference_answer_by) if example.reference_answer_by else "unknown",
                'reference_contexts': example.reference_contexts
            }
            qa_pairs.append(qa_pair)
        
        return qa_pairs

def main():
    """Entry point of the QA Generator."""
    try:
        # Initialize generator
        print("Initializing QA Generator...")
        generator = QAGenerator()
        
        # Load documents
        docs_dir = "./data/test_documents"
        print(f"\nLoading documents from {docs_dir}...")
        documents = generator.load_documents(docs_dir)
        print(f"Loaded {len(documents)} documents")
        
        # Generate questions
        print("\nGenerating questions...")
        qa_pairs = generator.generate_questions(documents, questions_per_chunk=5)
        print(f"Generated {len(qa_pairs)} question-answer pairs")
        
        # Print examples
        print("\nExample QA pairs:")
        for i, qa in enumerate(qa_pairs[:2], 1):
            print(f"\nPair {i}:")
            print(f"Query: {qa['query']}")
            print(f"Query By: {qa['query_by']}")
            print(f"Reference Answer: {qa['reference_answer']}")
            print(f"Reference Answer By: {qa['reference_answer_by']}")
            print(f"Number of Reference Contexts: {len(qa['reference_contexts'])}")
            
        # Save in different formats
        # 1. Save detailed JSON format with all information
        json_file = "generated_qa_pairs.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(qa_pairs, f, indent=2, ensure_ascii=False)
        print(f"\nSaved detailed QA pairs to {json_file}")
        
        # 2. Save questions-only format
        questions_file = "generated_questions.txt"
        with open(questions_file, "w", encoding="utf-8") as f:
            for qa in qa_pairs:
                f.write(f"{qa['query']}\n")
        print(f"Saved questions to {questions_file}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
