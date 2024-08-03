# import json
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import aiohttp
import re
import json


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

def get_lsa_summarizer():
    return LsaSummarizer()

def get_parser(text, lang='english'):
    return PlaintextParser.from_string(text, Tokenizer(lang))

def lsa_summarize_text(text, summarizer, num_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    # summarizer = LsaSummarizer()
    
    summary = summarizer(parser.document, num_sentences)
    summarized_text = ' '.join([str(sentence) for sentence in summary])
    return summarized_text

def clean_text_corpus(corpus):
    # text = corpus.replace('\r', ' ')
    text = corpus
    text = re.sub(r'[^A-Za-z\s]', '', text)
    text = ' '.join(text.split())
    return text


def llm_summarize(text, search_query, num_words=500):
    url = "http://localhost:11434/api/generate"
    body = {
        "model": "llama3.1:8b",
        "prompt": f"Given the following data scraped from the internet on the given query \"{search_query}\" \n Data scraped from the internet : {text} \n \
        Give a summary of the search in about {num_words} words don't use any html tags or special characters, give the search result in steps if it has a process and give a paragraph if it is a general question. \
        Generate the summary as if you are giving the search response. Phrase it as you are speaking. \
        Also assume the user does not have pre-requisite knowledge on the search query. \
        If the generated response needs to be larger to make the user understand things, don't worry about the word count, you can cross it." 
    }
    headers = {
        'Content-Type': 'application/json'
    }
    res = requests.post(url, headers=headers, data=json.dumps(body))

    res = str(res.content, encoding='utf-8')
    summary = ""
    for i in res.split('\n'):
        d = json.loads(i)
        if d["done"]:
            break
        # print(d["response"], end="")
        summary += d['response']
    return summary