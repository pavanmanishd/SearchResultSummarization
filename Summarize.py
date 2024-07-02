from bs4 import BeautifulSoup
import requests

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

# URL of the webpage
url = 'https://www.revelo.com/blog/how-to-make-an-ai'

# Fetch and print the paragraphs
paragraphs = fetch_and_extract_paragraphs(url)
if paragraphs:
    for para in paragraphs:
        print(para)
        print()  
