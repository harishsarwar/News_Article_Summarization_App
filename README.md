---->News article app <-----

# News Articles Powered by Groq

This is a Streamlit app that retrieves and summarizes news articles using Groq's large language model (LLM). Users can enter a topic, retrieve articles, generate summaries, and even write a draft article based on the summarized news.

## Features

- **Topic-based Search:** Enter a topic and fetch related news articles.
- **Summary Generation:** Summarize the fetched news articles with customizable word length.
- **Article Writing:** Generate a draft article using the summarized news content.
- **Groq LLM Integration:** Uses Groq's LLM for summarization and article generation.
- **Customizable Models:** Choose different models for summary and article writing.

## Installation

To run this app locally, clone this repository and install the required dependencies.

```bash
git clone https://github.com/yourusername/news-articles-powered-by-groq.git
cd news-articles-powered-by-groq
pip install -r requirements.txt

Setup Environment Variables

Create a .env file in the root directory.
Add your Groq API key:
GROQ_API_KEY=your_api_key_here

Usage
1.Run the Streamlit app:

streamlit run app.py

2.Open your browser and navigate to the local Streamlit server.

3.In the sidebar, choose the Summary Model and Writer Model, and adjust the search and summary settings as desired.

4.Enter a topic in the input field and click Write Article to fetch and summarize news articles, followed by article generation.


Requirements

Python 3.x
Streamlit
DuckDuckGo Search
Groq API integration (langchain_groq)
dotenv



