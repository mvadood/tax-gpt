import streamlit as st
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.chat_engine.types import ChatMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

import secret

st.set_page_config(page_title="Ask your Tax Questions", page_icon="💰", layout="centered", initial_sidebar_state="auto",
                   menu_items=None)

st.title("Ask your Tax Questions 💬")
st.info("https://www.linkedin.com/in/mvadood/", icon="🧑")

Settings.llm = Ollama(model="llama3", request_timeout=360.0)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Tax and Tax Return in Australia. 🇦🇺🦘🦙"},
    ]

pinecone = Pinecone(api_key=secret.pinecone_api_key)
pinecone_index = pinecone.Index("ato")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
vector_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading the ATO docs index – hang tight! This will take a few moments."):
        return vector_index


index = load_data()

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = index.as_chat_engine(chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT, verbose=True)


def classify_question(prompt):
    # classification_prompt = f"Is the following question related to tax or tax returns in Australia? Answer 'yes' or 'no'.\n\nQuestion: {prompt}"
    # response = st.session_state.chat_engine.chat(classification_prompt)
    # return "yes" in response.response.lower()
    return "yes"


if prompt := st.chat_input("your question:"):
    if classify_question(prompt):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chat_engine.chat(prompt)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)
    else:
        st.session_state.messages.append({"role": "assistant",
                                          "content": "I'm here to answer questions about tax and tax returns in Australia. Please ask a relevant question."})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
