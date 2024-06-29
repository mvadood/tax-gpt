import os  # Import os module for environment variables

from llama_index.core import Settings, StorageContext  # Import Settings and StorageContext from llama_index.core
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader  # Import VectorStoreIndex and SimpleDirectoryReader from llama_index.core
from llama_index.embeddings.huggingface import HuggingFaceEmbedding  # Import HuggingFaceEmbedding from llama_index.embeddings.huggingface
from llama_index.llms.ollama import Ollama  # Import Ollama from llama_index.llms.ollama
from llama_index.vector_stores.pinecone import PineconeVectorStore  # Import PineconeVectorStore from llama_index.vector_stores.pinecone
from pinecone import Pinecone  # Import Pinecone client from pinecone

import secret

pc = Pinecone(api_key=secret.pinecone_api_key)  # Initialize Pinecone client with the API key


def create_and_store_index():
    # Create a SimpleDirectoryReader instance to read documents from specified directory
    reader = SimpleDirectoryReader(input_dir="taxScrapy/output_files", recursive=True)
    docs = reader.load_data()  # Load data/documents from the specified directory

    # Create a Pinecone index named "ato"
    pinecone_index = pc.Index("ato")

    # Create a PineconeVectorStore instance using the Pinecone index
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

    # Create a StorageContext instance with default settings and the PineconeVectorStore
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Set the HuggingFace embedding model to BAAI/bge-base-en-v1.5
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

    # Set the Ollama model to llama3 with a request timeout of 360 seconds
    Settings.llm = Ollama(model="llama3", request_timeout=360.0)

    # Create a VectorStoreIndex using the loaded documents and the StorageContext
    index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)


if __name__ == "__main__":
    create_and_store_index()  # Execute the create_and_store_index function if this script is run directly
