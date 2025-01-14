import nest_asyncio
from typing import Optional


import streamlit as st
from duckduckgo_search import DDGS
from phi.tools.newspaper4k import Newspaper4k

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


# load environment

load_dotenv()

# Get the Groq API key from the .env file
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("Groq API key not found. Please set it in the .env file.")

# Initialize the Groq client
groq_client = ChatGroq(api_key=groq_api_key)

# Apply nest_asyncio for Streamlit compatibility
nest_asyncio.apply()

# streamlit app cofiguration.
st.set_page_config(
    page_title="News Article",
    page_icon=":orange_heart",
)

st.title("News Article powered by groq")
st.markdown("#### : orange_heart: Built using groq LLM model")

# trncate text
def truncate_text(text: str, words: int) -> str:
    return " ".join(text.split()[:words])


# main fuction:
def main() ->None:
    # slider
    summary_model = st.sidebar.selectbox(
        "select summary model", options=["llama3-8b-8192", "mixtral-8x7b-32768", "llama3-70b-8192"]  
    )
    writer_model = st.slider.selectbox(
        "select writer model", options=["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"]
    )


    # research options
    st.sidebar.markdown("## research options")
    num_search_result= st.sidebar.slider(
        ":sparkles: number of search results",
        min_value=3,
        max_value=20,
        value=7,
        help="number of results"
    )
    per_article_summary_length = st.sidebar.slider(
        ":sparkles: number of article",
        min_value=100,
        max_value=2000,
        value=800,
        help="number of qrod per article"
    )

    news_summary_length = st.sidebar.slider(
        ":sparkles: length of draft",
        min_value=1000,
        max_value=10000,
        value=5000,
        step=100,
        help="number of word in the draft article"
    )

    # topic imput

    article_topic = st.text_input(
        ":spiral_claendar_pad: enter a topic",
        value="ai and its impact",
        )
    write_article = st.button("write aricle")
    if write_article:
        news_results = []
        news_summary: Optional[str] = None
        with st.status("reading news", expanded=False) as status:
            with st.container():
                news_container = st.empty()
                ddgs = DDGS()
                newspaper_tools = Newspaper4k()
                results = ddgs.news(keywords=article_topic, max_results=num_search_results)
                for r in results:
                    if "url" in r:
                        article_data = newspaper_tools.get_article_data(r["url"])
                        if article_data and "text" in article_data:
                            r["text"] = article_data["text"]
                            news_results.append(r)
                            if news_results:
                                news_container.write(news_results)
            if news_results:
                news_container.write(news_results)
            status.update(label="News Search Complete", state="complete", expanded=False)

        # Summarize news results
        if len(news_results) > 0:
            news_summary = ""
            with st.status("Summarizing News", expanded=False) as status:
                with st.container():
                    summary_container = st.empty()
                    for news_result in news_results:
                        news_summary += f"### {news_result['title']}\n\n"
                        news_summary += f"- Date: {news_result['date']}\n\n"
                        news_summary += f"- URL: {news_result['url']}\n\n"
                        news_summary += f"#### Introduction\n\n{news_result['text'][:500]}\n\n"

                        # Use Groq API to generate summary
                        prompt = "Summarize the following article:\n" + news_result['text']
                        response = groq_client.invoke(input=prompt, model=summary_model)
                        
                        _summary = response.content.strip()
                        _summary_length = len(_summary.split())
                        if _summary_length > news_summary_length:
                            _summary = truncate_text(_summary, news_summary_length)
                        news_summary += "#### Summary\n\n"
                        news_summary += _summary
                        news_summary += "\n\n---\n\n"
                        if news_summary:
                            summary_container.markdown(news_summary)
                        if len(news_summary.split()) > news_summary_length:
                            break

                if news_summary:
                    summary_container.markdown(news_summary)
                status.update(label="News Summarization Complete", state="complete", expanded=False)

        if news_summary is None:
            st.write("Sorry, could not find any news or web search results. Please try again.")
            return

        # Generate article draft
        article_draft = f"# Topic: {article_topic}\n\n"
        if news_summary:
            article_draft += "## Summary of News Articles\n\n"
            article_draft += f"This section provides a summary of the news articles about {article_topic}.\n\n"
            article_draft += news_summary + "\n\n"

        with st.status("Writing Draft", expanded=True) as status:
            st.markdown(article_draft)
            status.update(label="Draft Complete", state="complete", expanded=False)

        with st.spinner("Writing Article..."):
            # Use Groq API to write the article
            prompt = f"Write an article about {article_topic} using the following summary:\n{news_summary}"
            response = groq_client.invoke(input=prompt, model=writer_model)
            final_report = response.content.strip()
            st.markdown(final_report)

    st.sidebar.markdown("---")
    if st.sidebar.button("Restart"):
        st.experimental_rerun()

main()


    






