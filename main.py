import os
from dotenv import load_dotenv
import asyncio
from concurrent.futures import ThreadPoolExecutor

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

text_corpus = ""

def fetch_data(link):
    content = asyncio.run(fetch_and_extract_paragraphs(link))
    return content

async def main():
    search_string = input('Enter a search query: ')
    
    search_result = await search_query(search_string, API_KEY, SEARCH_ENGINE_ID)
    links = extract_links(search_result)

    # Use ThreadPoolExecutor to fetch data concurrently
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_data, link) for link in links]
        results = [future.result() for future in futures]

    global text_corpus
    text_corpus = "\n".join(filter(None, results))

    with open("text_corpus.txt", "w") as tf:
        tf.write(text_corpus)


    print(len(text_corpus))

    parser = get_parser(text_corpus)
    summarizer = get_summarizer()

    summary = summarize_text(text_corpus, summarizer, num_sentences=10)

    print("Summary: ")
    print(summary)

if __name__ == '__main__':
    asyncio.run(main())
