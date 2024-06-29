The repository contains the necessary code for building a simple RAG based on data scraped from [ATO](https://www.ato.gov.au/).

Read more details [here](https://medium.com/theladlab/a-chatbot-for-your-tax-return-part-1-intro-web-crawler-377801c1beae).

* `pip install -r requirements.txt` to install dependencies
* Set necessary secrets in `secret.py`. If you're deploying onto [Streamlit community](https://streamlit.io/community), don't forget to set the keys before deployment. Otherwise, hard-code the keys.

**To Run the Scraper**

`scrapy crawl tax -a max_depth=1`

Adjust `max_depth` as required.


**Files Description**
* `create_index.py`: Build a local index using [llana_index](https://github.com/run-llama/llama_index) and GPT-4 off scraped data and store locally.
* `chatbot.py`: [Streamlit](https://github.com/streamlit/streamlit) code for bringing up a GPT chatbot locally. Run `streamlit run chatbot.py` for loading the UI.
* `create_index_for_llama.py`: Code for vectorising scraped data using [BAAI/bge-base-en-v1.5](https://huggingface.co/BAAI/bge-base-en-v1.5) and storing the index locally.
* `chatbot_llama.py`: [Streamlit](https://github.com/streamlit/streamlit) code for bringing up an [Ollama](https://github.com/ollama/ollama)-based chatbot locally. Run `streamlit run chatbot_llama.py` for loading the UI.
* `create_index_pinecone`: Code for vectorising scraped data using [BAAI/bge-base-en-v1.5](https://huggingface.co/BAAI/bge-base-en-v1.5) and storing the index in [Pinecone](https://www.pinecone.io/).
* `chatbot_llama_pinecone.py`: [Streamlit](https://github.com/streamlit/streamlit) code for bringing up an [Ollama](https://github.com/ollama/ollama)-based chatbot locally. Pinecone is queried for retrieving context. Run `streamlit run chatbot_llama_pinecone.py` for loading the UI.
* `chatbot_groq_pinecone.py`: [Streamlit](https://github.com/streamlit/streamlit) code for bringing up a [Groq](https://groq.com)-based chatbot. Pinecone is queried for retrieving context. Run `streamlit run chatbot_groq_pinecone.py` for loading the UI. Same file can be used to deploy the chatbot to [Streamlit community](https://streamlit.io/community).