import streamlit as st  # Import Streamlit library for building web apps
from llama_index.core.chat_engine.types import ChatMode  # Import ChatMode enum from llama_index
from llama_index.embeddings.huggingface import HuggingFaceEmbedding  # Import HuggingFaceEmbedding from llama_index
from llama_index.llms.ollama import Ollama  # Import Ollama class from llama_index

from llama_index.core import StorageContext, load_index_from_storage, Settings  # Import necessary components

# Configure Streamlit page settings
st.set_page_config(page_title="Ask your Tax Questions", page_icon="💰", layout="centered", initial_sidebar_state="auto",
                   menu_items=None)

# Set title of the app
st.title("Ask your Tax Questions 💬")
st.info("https://www.linkedin.com/in/mvadood/", icon="🧑")
# Set Ollama model and HuggingFace embedding model for tax-related questions
Settings.llm = Ollama(model="llama3", request_timeout=360.0)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

# Initialize chat messages history if not already initialized
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Tax and Tax Return in Australia. 🇦🇺🦘🦙"},
    ]


# Function to load data from ATO docs index and cache it
@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading the ATO docs index – hang tight! This will take a few moments."):
        storage_context = StorageContext.from_defaults(persist_dir="index")
        loaded_index = load_index_from_storage(storage_context)
        return loaded_index


# Load data from ATO docs index
index = load_data()

# Initialize chat engine if not already initialized
if "chat_engine" not in st.session_state.keys():
    st.session_state.chat_engine = index.as_chat_engine(chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT, verbose=True)


# Function to classify user's question as related to tax in Australia
def classify_question(prompt):
    classification_prompt = f"Is the following question related to tax or tax returns in Australia? Answer 'yes' or 'no'.\n\nQuestion: {prompt}"
    response = st.session_state.chat_engine.chat(classification_prompt)
    return "yes" in response.response.lower()


# Get user input question
if prompt := st.chat_input("your question:"):
    if classify_question(prompt):  # If question is related to tax, process it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chat_engine.chat(prompt)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)
    else:  # If question is not related to tax, provide guidance
        st.session_state.messages.append({"role": "assistant",
                                          "content": "I'm here to answer questions about tax and tax returns in Australia. Please ask a relevant question."})

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
