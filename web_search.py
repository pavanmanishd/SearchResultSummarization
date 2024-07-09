import requests
from bs4 import BeautifulSoup
import json

# Replace 'YOUR_API_KEY' and 'YOUR_SEARCH_ENGINE_ID' with your actual API key and Search Engine ID
API_KEY = 'AIzaSyCRfPE6noHguT5nrXQvBXN7SRrFHBqM9GY'
SEARCH_ENGINE_ID = '20ac1cd0a17f047f1'

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

if __name__ == '__main__':
    # search_term = input('Enter the search string: ')
    search_term = "How to build an ai bot"
    search_results = google_search(search_term, API_KEY, SEARCH_ENGINE_ID)
    links = extract_links(search_results)
    save_links_to_file(links)
    print(f'Saved {len(links)} links to output.txt')
    print("This line is inserted in vim editor")
