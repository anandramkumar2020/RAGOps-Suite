from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.settings import Settings
from llama_index.core.node_parser import SimpleNodeParser
import openai
import chromadb
import os
from dotenv import load_dotenv
from typing import List
import shutil

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Set up paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)

# Initialize ChromaDB and vector store
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
chroma_collection = chroma_client.get_or_create_collection("ragops")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Global variable to store the index
index = None

def initialize_index():
    """Initialize or reload the index from documents in the data directory"""
    global index
    try:
        # Initialize ChromaDB
        chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
        chroma_collection = chroma_client.get_or_create_collection("documents")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Try to load documents from the data directory
        try:
            documents = SimpleDirectoryReader(DATA_DIR).load_data()
            index = VectorStoreIndex.from_documents(
                documents,
                storage_context=storage_context
            )
        except ValueError as e:
            # If no documents found, create an empty index
            index = VectorStoreIndex([], storage_context=storage_context)
            print("Created empty index - no documents found.")
    except Exception as e:
        print(f"Error initializing index: {str(e)}")
        raise e

# Initialize the index on startup
initialize_index()

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file to the data directory and update the index"""
    try:
        # Save the file to the data directory
        file_path = os.path.join(DATA_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Reload the index
        initialize_index()
        
        return {"message": f"Successfully uploaded {file.filename} and updated index"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reload")
async def reload_index():
    """Reload the index with all documents in the data directory"""
    try:
        initialize_index()
        return {"message": "Index reloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/query")
async def query_index(query_text: str):
    """Query the index"""
    try:
        if not index:
            raise HTTPException(status_code=500, detail="Index not initialized")
        
        # Query the index
        query_engine = index.as_query_engine()
        response = query_engine.query(query_text)
        
        # Extract context metadata with text preview
        source_nodes = response.source_nodes
        contexts = []
        
        for node in source_nodes:
            # Get first 100 characters of text as preview
            text_preview = node.node.text[:100] + "..." if len(node.node.text) > 100 else node.node.text
            
            # Get all metadata and filter out None values
            metadata = {
                k: v for k, v in node.node.metadata.items() 
                if v is not None
            }
            
            # Add node info
            node_info = {
                "file_name": metadata.get("file_name", "Unknown"),
                "score": float(node.score) if node.score else None,
                "text_preview": text_preview,
                "metadata": metadata
            }
            
            contexts.append(node_info)
        
        return {
            "response": str(response),
            "contexts": contexts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents")
async def list_documents():
    """List all documents in the data directory"""
    try:
        documents = []
        for filename in os.listdir(DATA_DIR):
            file_path = os.path.join(DATA_DIR, filename)
            if os.path.isfile(file_path):
                documents.append({
                    "name": filename,
                    "size": os.path.getsize(file_path),
                    "last_modified": os.path.getmtime(file_path)
                })
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
