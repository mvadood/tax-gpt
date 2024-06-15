import streamlit as st
import openai

import secret

openai.api_key = secret.open_ai_api_key

from llama_index.core import SimpleDirectoryReader, ServiceContext, VectorStoreIndex, StorageContext, \
    load_index_from_storage

st.set_page_config(page_title="Ask your Tax Questions", page_icon="💰", layout="centered", initial_sidebar_state="auto",
                   menu_items=None)

st.title("Ask your Tax Questions 💬")
st.info("https://www.linkedin.com/in/mvadood/", icon="🧑")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Tax and Tax Return in Australia. 🇦🇺🦘🦙"},
    ]


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading the ATO docs index – hang tight! This will take a few moments."):
        storage_context = StorageContext.from_defaults(persist_dir="index")
        loaded_index = load_index_from_storage(storage_context)
        return loaded_index


index = load_data()

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("your question:"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)
