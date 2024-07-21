# import json
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import aiohttp


async def search_query(search_term, api_key, search_engine_id):
    url = f'https://www.googleapis.com/customsearch/v1?q={search_term}&key={api_key}&cx={search_engine_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            results = await response.json()
            return results

def extract_links(search_results):
    links = []
    for item in search_results.get('items', []):
        links.append(item.get('link'))
    return links

def save_links_to_file(links, filename='output.txt'):
    with open(filename, 'w') as file:
        for link in links:
            file.write(link + '\n')

# Function to fetch and extract paragraphs from a URL

async def fetch_and_extract_paragraphs(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Failed to retrieve the page. Status code: {response.status}")
                return None
            
            soup = BeautifulSoup(await response.text(), 'html.parser')
            paragraphs = soup.find_all('p')
            return "\n".join(para.get_text() for para in paragraphs)

def get_summarizer():
    return LsaSummarizer()

def get_parser(text, lang='english'):
    return PlaintextParser.from_string(text, Tokenizer(lang))

def summarize_text(text, summarizer, num_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    # summarizer = LsaSummarizer()
    
    summary = summarizer(parser.document, num_sentences)
    summarized_text = ' '.join([str(sentence) for sentence in summary])
    return summarized_text

if __name__ == '__main__':
    # search_term = input('Enter the search string: ')
    search_term = "How to build an ai bot"
    # search_results = search_query(search_term, API_KEY, SEARCH_ENGINE_ID)
    links = extract_links(search_results)
    save_links_to_file(links)
    print(f'Saved {len(links)} links to output.txt')
    print("This line is inserted in vim editor")
