import openai  # Importing OpenAI for natural language processing
import streamlit as st  # Importing Streamlit for creating web apps

import secret  # Importing secret module for API key

# Setting OpenAI API key
openai.api_key = secret.open_ai_api_key

from llama_index.core import StorageContext, load_index_from_storage  # Importing custom modules

# Configuring Streamlit page settings
st.set_page_config(
    page_title="Ask your Tax Questions",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

# Adding title to the web app
st.title("Ask your Tax Questions 💬")

# Adding info message with a link to LinkedIn profile
st.info("https://www.linkedin.com/in/mvadood/", icon="🧑")

# Initializing chat messages history if not already present
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Tax and Tax Return in Australia. 🇦🇺🦘🦙"},
    ]

# Function to load data from storage (caching to avoid repeated loading)
@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading the ATO docs index – hang tight! This will take a few moments."):
        storage_context = StorageContext.from_defaults(persist_dir="index")
        loaded_index = load_index_from_storage(storage_context)
        return loaded_index

# Loading data into 'index'
index = load_data()

# Initializing chat engine if not already present
if "chat_engine" not in st.session_state.keys():
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

# Handling user input in the chat interface
if prompt := st.chat_input("your question:"):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Displaying chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Checking if the last message is from the assistant to initiate response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)
