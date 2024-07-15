# import json
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

load_dotenv()

API_KEY = os.environ["API_KEY"]
SEARCH_ENGINE_ID = os.environ["SEARCH_ENGINE_ID"]


def google_search(search_term, api_key, search_engine_id):
    url = f'https://www.googleapis.com/customsearch/v1?q={search_term}&key={api_key}&cx={search_engine_id}'
    response = requests.get(url)
    results = response.json()
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
def fetch_and_extract_paragraphs(url):
    # Fetch the webpage
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all paragraph tags
    paragraphs = soup.find_all('p')
    
    # Extract and return the text from each paragraph
    content = [para.get_text() for para in paragraphs]
    return content

# Function to summarize text
def summarize_text(text, num_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    
    summary = summarizer(parser.document, num_sentences)
    summarized_text = ' '.join([str(sentence) for sentence in summary])
    return summarized_text

if __name__ == '__main__':
    # search_term = input('Enter the search string: ')
    search_term = "How to build an ai bot"
    search_results = google_search(search_term, API_KEY, SEARCH_ENGINE_ID)
    links = extract_links(search_results)
    save_links_to_file(links)
    print(f'Saved {len(links)} links to output.txt')
    print("This line is inserted in vim editor")
