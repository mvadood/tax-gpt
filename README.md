This is the code for this [YouTube](https://studio.youtube.com/video/CsO6iUKHKwU) Tutorial.


The code contains a simple GPT wrapper that is contextualised using data scraped from the [ATO website](https://www.ato.gov.au).


**To Run**

1. `pip install -r requirements.txt`
2. Create an API Key in [OpenAI](https://platform.openai.com/api-keys).
3. Set the API Key in `secret.py`.
4. Run `create_index.py` to create the index.
5. `streamlit run chatbot.py` to bring up the bot.

