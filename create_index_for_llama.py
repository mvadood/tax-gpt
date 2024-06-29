from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

def create_and_store_index():
    # Initialize SimpleDirectoryReader to read documents from directory
    reader = SimpleDirectoryReader(input_dir="taxScrapy/output_files", recursive=True)
    docs = reader.load_data()  # Load documents from specified directory

    # Set HuggingFace embedding model (bge-base)
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

    # Set Ollama LLM with specific model and timeout
    Settings.llm = Ollama(model="llama3", request_timeout=360.0)

    # Create VectorStoreIndex from loaded documents
    index = VectorStoreIndex.from_documents(docs)

    # Persist the index to disk
    index.storage_context.persist(persist_dir="index")

if __name__ == "__main__":
    create_and_store_index()  # Execute the function to create and store the index
