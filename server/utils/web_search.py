# import json
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import aiohttp
import re
import json

async def search_query(search_term, api_key, search_engine_id):
    url = f'https://www.googleapis.com/customsearch/v1?q={search_term}&key={api_key}&cx={search_engine_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
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
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Failed to retrieve the page. Status code: {response.status}")
                    return None
                
                soup = BeautifulSoup(await response.text(), 'html.parser')
                paragraphs = soup.find_all('p')
                return "\n".join(para.get_text() for para in paragraphs)
    except:
        pass

def clean_text_corpus(corpus):
    # text = corpus.replace('\r', ' ')
    text = corpus
    text = re.sub(r'[^A-Za-z\s]', '', text)
    text = ' '.join(text.split())
    return text


def llm_summarize_llama(text, search_query, num_words=750):
    url = "http://localhost:11434/api/generate"
    body = {
        "model": "llama3.1:8b",
        "prompt": f"Given the following data scraped from the internet on the given query:  \"{search_query}\" \n Data scraped from the internet : {text} \n \
        Give a summary of the search in about {num_words} words don't use any special characters, give the search result in steps if it has a process and give a paragraph if it is a general question. \
        If the data from the internet doesn't seem relevant to the search query, use your own knowledge to make the answer relevant to the search query. \
        Use markup to generate the response, do NOT use any html tags."
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

def gemini_summarizer(text, search_query, num_words=750):
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
    params = {
        'key': os.getenv('API_KEY')
    }
    prompt = f"Given the following data from the internet on the given query:  \"{search_query}\" \n Data from the internet : {text} \n \
        Give a summary of the search in about {num_words} words. Don't use any special characters. \
        If the data from the internet doesn't seem relevant to the search query, use your own knowledge to make the answer relevant to the search query. \
        Use markup to generate the response, do NOT use any html tags."
    body = {
        'contents': [
            {
                'parts': [{
                    'text': prompt
                }]
            }
        ]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    res = requests.post(url, headers=headers, params=params, data=json.dumps(body))
    res = res.json()
    result = res['candidates'][0]['content']['parts'][0]['text']

    return result