from llama_index.core import SimpleDirectoryReader, ServiceContext, VectorStoreIndex
import openai  # Import OpenAI library
from llama_index.llms.openai import OpenAI  # Import OpenAI LLM from llama_index.llms

import secret  # Import secret module for API keys

# Set OpenAI API key
openai.api_key = secret.open_ai_api_key

def create_and_store_index():
    # Initialize SimpleDirectoryReader to read documents from directory
    reader = SimpleDirectoryReader(input_dir="taxScrapy/output_files", recursive=True)
    docs = reader.load_data()  # Load documents from specified directory

    # Define service context for OpenAI LLM
    service_context = ServiceContext.from_defaults(
        llm=OpenAI(
            model="gpt-4",
            temperature=0.5,
            system_prompt="You are an expert on the Australian Tax Laws and your job is to answer questions related to tax. "
                          "Assume that all questions are related to tax return in Australia in July 2024. "
                          "Keep your answers technical and based on facts – do not hallucinate features."
        )
    )

    # Create VectorStoreIndex from documents using the specified service context
    index = VectorStoreIndex.from_documents(docs, service_context=service_context)

    # Persist the index to disk
    index.storage_context.persist(persist_dir="index")

if __name__ == "__main__":
    create_and_store_index()  # Execute the function to create and store the index
