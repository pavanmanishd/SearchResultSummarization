import os
from dotenv import load_dotenv
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading

from utils.web_search import (
    search_query,
    extract_links,
    fetch_and_extract_paragraphs,
    clean_text_corpus,
    llm_summarize,
    save_links_to_file
)

load_dotenv()

API_KEY = os.environ["API_KEY"]
SEARCH_ENGINE_ID = os.environ["SEARCH_ENGINE_ID"]

text_corpus = ""

def fetch_data(link, results):
    content = asyncio.run(fetch_and_extract_paragraphs(link))
    # return content
    results.append(content)

def main():
    search_string = input('Enter a search query: ')
    
    search_result = asyncio.run(search_query(search_string, API_KEY, SEARCH_ENGINE_ID))
    links = extract_links(search_result)
    save_links_to_file(links)

    results = []
    threads = []
    for link in links:
        thread = threading.Thread(target=fetch_data, args=[link, results])
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    
    global text_corpus
    text_corpus = "\n".join(filter(None, results))

    cleaned_text = clean_text_corpus(text_corpus)
    with open("text_corpus.txt", "w") as tf:
        tf.write(cleaned_text)


    print(len(text_corpus), len(cleaned_text))

    summary = llm_summarize(text=text_corpus, search_query=search_string)

    # print(summary)
    with open("summary.md", "w") as f:
        f.write(summary)

    # parser = get_parser(text_corpus)
    # summarizer = get_lsa_summarizer()

    # summary = lsa_summarize_text(text_corpus, summarizer, num_sentences=10)

    # print("Summary: ")
    # print(summary)

if __name__ == '__main__':
    main()
