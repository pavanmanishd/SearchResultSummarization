import os
from dotenv import load_dotenv
import asyncio
from utils.web_search import (
    search_query, 
    extract_links, 
    fetch_and_extract_paragraphs, 
    get_summarizer,
    summarize_text,
    get_parser
)


load_dotenv()

API_KEY = os.environ["API_KEY"]
SEARCH_ENGINE_ID = os.environ["SEARCH_ENGINE_ID"]

async def main():
    search_string = input('Enter a search query: ')

    search_result = await search_query(search_string, API_KEY, SEARCH_ENGINE_ID)
    links = extract_links(search_result)

    text_corpus = ""
    for link in links:
        content = await fetch_and_extract_paragraphs(link)
        text_corpus += content + "\n"

    print(len(text_corpus))

    parser = get_parser(text_corpus)
    summarizer = get_summarizer()

    summary = summarize_text(text_corpus, summarizer, num_sentences=10)

    print("Summary: ")
    print(summary)

if __name__ == '__main__':
    asyncio.run(main())
        