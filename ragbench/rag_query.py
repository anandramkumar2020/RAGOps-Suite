"""
Simple RAG Query Client
"""

import aiohttp
import asyncio
from typing import Dict, Any, Optional

class RagClient:
    def __init__(self, api_endpoint: str = "http://localhost:8000"):
        self.api_endpoint = api_endpoint.rstrip('/')

    async def query(self, question: str) -> Optional[Dict[str, Any]]:
        """Send query to RAG application and get response."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_endpoint}/api/query",
                    params={"query_text": question}
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data
        except aiohttp.ClientError as e:
            print(f"Error querying RAG endpoint: {e}")
            return None

async def main():
    client = RagClient()
    question = "What is machine learning?"
    
    response = await client.query(question)
    if response:
        print(f"\nQuestion: {question}")
        print(f"Answer: {response['response']}")
        print("\nContexts:")
        for ctx in response['contexts']:
            print(f"\nFile: {ctx['file_name']}")
            print(f"Score: {ctx['score']}")
            print(f"Preview: {ctx['text_preview']}")

if __name__ == "__main__":
    asyncio.run(main())