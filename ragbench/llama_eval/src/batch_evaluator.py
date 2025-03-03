"""
Batch RAG Evaluator Module

This module implements batch evaluation of RAG responses using multiple evaluators:
1. Faithfulness Evaluation - Evaluates if the response is consistent with the provided context
2. Relevancy Evaluation - Evaluates if the response is relevant to the query
3. Context Relevancy - Evaluates if retrieved contexts are relevant to the query
"""

import json
import aiohttp
from typing import Dict, List, Any
from pathlib import Path
from dotenv import load_dotenv
import os
import asyncio
import nest_asyncio
import pandas as pd
from datetime import datetime
from llama_index.llms.openai import OpenAI
from llama_index.core.evaluation import (
    FaithfulnessEvaluator,
    RelevancyEvaluator,
    BatchEvalRunner
)

# Apply nest_asyncio to handle nested event loops
nest_asyncio.apply()

class BatchRagEvaluator:
    """Batch evaluator for RAG application responses."""
    
    def __init__(self, api_endpoint: str = "http://localhost:8000"):
        """Initialize batch RAG evaluator.
        
        Args:
            api_endpoint: Base URL of the RAG API
        """
        # Load environment variables
        load_dotenv()
        
        # Initialize OpenAI configuration
        self.llm = OpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.api_endpoint = api_endpoint
        
        # Initialize evaluators
        self.faithfulness_evaluator = FaithfulnessEvaluator(llm=self.llm)
        self.relevancy_evaluator = RelevancyEvaluator(llm=self.llm)
        self.context_relevancy_evaluator = RelevancyEvaluator(llm=self.llm)
        
        # Initialize batch runner
        self.batch_runner = BatchEvalRunner(
            evaluators={
                "faithfulness": self.faithfulness_evaluator,
                "relevancy": self.relevancy_evaluator,
                "context_relevancy": self.context_relevancy_evaluator
            },
            workers=8
        )
            
    def load_qa_pairs(self, qa_file: str = "generated_qa_pairs.json") -> List[Dict[str, Any]]:
        """Load generated QA pairs from JSON file.
        
        Args:
            qa_file: Path to the JSON file containing QA pairs
            
        Returns:
            List of QA pairs with queries and reference contexts
        """
        qa_path = Path(qa_file)
        if not qa_path.exists():
            raise FileNotFoundError(f"QA pairs file not found: {qa_file}")
            
        with open(qa_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    async def query_rag(self, query: str) -> Dict[str, Any]:
        """Send query to RAG application and get response.
        
        Args:
            query: Question to send to RAG
            
        Returns:
            RAG response containing answer and metadata
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_endpoint}/api/query",
                    params={"query_text": query}
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            print(f"Error querying RAG endpoint: {e}")
            return None

    async def evaluate_query(self, query: str, response: str, contexts: List[str]) -> Dict[str, Any]:
        """Evaluate a single query using faithfulness, relevancy, and context relevancy metrics.
        
        Args:
            query: The original query
            response: The RAG system's response
            contexts: List of context strings used to generate the response
            
        Returns:
            Dictionary containing evaluation results from all evaluators
        """
        try:
            # Evaluate faithfulness
            faith_result = await self.faithfulness_evaluator.aevaluate(
                query=query,
                response=response,
                contexts=contexts
            )
            
            # Evaluate answer relevancy
            rel_result = await self.relevancy_evaluator.aevaluate(
                query=query,
                response=response,
                contexts=contexts
            )
            
            # Evaluate context relevancy for each context
            context_rel_results = []
            for context in contexts:
                ctx_result = await self.context_relevancy_evaluator.aevaluate(
                    query=query,
                    response=context,  # Treat context as response to check relevancy
                    contexts=[context]  # Pass context as its own context
                )
                context_rel_results.append(ctx_result)
            
            # Calculate average context relevancy score
            avg_context_score = sum(r.score for r in context_rel_results) / len(context_rel_results) if context_rel_results else 0
            context_passing = all(r.passing for r in context_rel_results) if context_rel_results else False
            
            return {
                "faithfulness": faith_result,
                "relevancy": rel_result,
                "context_relevancy": {
                    "score": avg_context_score,
                    "passing": context_passing,
                    "individual_results": context_rel_results
                }
            }
        except Exception as e:
            print(f"Error during evaluation: {e}")
            return None

async def main():
    """Entry point for batch RAG evaluation."""
    try:
        # Initialize evaluator
        print("Initializing batch RAG evaluator...")
        evaluator = BatchRagEvaluator()
        
        # Load QA pairs
        print("\nLoading generated QA pairs...")
        qa_pairs = evaluator.load_qa_pairs(r"D:\RAGOps-Workspace\RAGOps-Suite\ragbench\llama_eval\generated_qa_pairs.json")
        print(f"Loaded {len(qa_pairs)} QA pairs")
        
        # Create DataFrame to store results
        results_data = []
        
        # Process all queries
        print("\nProcessing queries and running evaluations...")
        print("-" * 80)
        
        for qa_pair in qa_pairs:
            query = qa_pair['query']
            contexts = qa_pair['reference_contexts']
            
            try:
                # Get RAG response
                rag_response = await evaluator.query_rag(query)
                if rag_response:
                    response_text = rag_response.get("response", "")
                    
                    # Run evaluation
                    eval_results = await evaluator.evaluate_query(
                        query=query,
                        response=response_text,
                        contexts=contexts
                    )
                    
                    # Store results in DataFrame
                    results_data.append({
                        'timestamp': datetime.now().isoformat(),
                        'query': query,
                        'response': response_text,
                        'context': contexts[0] if contexts else "",
                        'faithfulness_score': eval_results['faithfulness'].score,
                        'faithfulness_passing': eval_results['faithfulness'].passing,
                        'faithfulness_feedback': eval_results['faithfulness'].feedback,
                        'relevancy_score': eval_results['relevancy'].score,
                        'relevancy_passing': eval_results['relevancy'].passing,
                        'relevancy_feedback': eval_results['relevancy'].feedback,
                        'context_relevancy_score': eval_results['context_relevancy']['score'],
                        'context_relevancy_passing': eval_results['context_relevancy']['passing']
                    })
                    
                    # Print results
                    print(f"\nQuery: {query}")
                    print(f"Response: {response_text[:200]}...")  # Show first 200 chars
                    print("Contexts:")
                    for ctx in contexts:
                        print(f"- {ctx[:200]}...")  # Show first 200 chars
                    print("\nEvaluation Results:")
                    print(f"Faithfulness: {eval_results['faithfulness']}")
                    print(f"Answer Relevancy: {eval_results['relevancy']}")
                    print(f"Context Relevancy Score: {eval_results['context_relevancy']['score']:.2f} (Passing: {eval_results['context_relevancy']['passing']})")
                    print("-" * 80)
                    
            except Exception as e:
                print(f"Error processing query '{query}': {str(e)}")
                continue
        
        # Create DataFrame and calculate statistics
        df = pd.DataFrame(results_data)
        
        # Calculate summary statistics
        summary_stats = {
            'Total Queries': len(df),
            'Average Faithfulness Score': df['faithfulness_score'].mean(),
            'Average Answer Relevancy Score': df['relevancy_score'].mean(),
            'Average Context Relevancy Score': df['context_relevancy_score'].mean(),
            'Passing Faithfulness': df['faithfulness_passing'].sum(),
            'Passing Answer Relevancy': df['relevancy_passing'].sum(),
            'Passing Context Relevancy': df['context_relevancy_passing'].sum()
        }
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_dir = Path('evaluation_results')
        results_dir.mkdir(exist_ok=True)
        
        # Save detailed results
        results_file = results_dir / f"evaluation_results_{timestamp}.csv"
        df.to_csv(results_file, index=False)
        
        # Save summary
        summary_file = results_dir / f"evaluation_summary_{timestamp}.csv"
        pd.DataFrame([summary_stats]).to_csv(summary_file, index=False)
        
        # Print summary
        print("\nEvaluation Summary:")
        for metric, value in summary_stats.items():
            print(f"{metric}: {value:.2f}")
        print(f"\nResults saved to:")
        print(f"Detailed results: {results_file}")
        print(f"Summary: {summary_file}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
