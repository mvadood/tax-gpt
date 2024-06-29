from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama


def create_and_store_index():
    reader = SimpleDirectoryReader(input_dir="taxScrapy/output_files", recursive=True)
    docs = reader.load_data()

    # bge-base embedding model
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

    # ollama
    Settings.llm = Ollama(model="llama3", request_timeout=360.0)

    index = VectorStoreIndex.from_documents(
        docs,
    )
    index.storage_context.persist(persist_dir="index")


if __name__ == "__main__":
    create_and_store_index()
