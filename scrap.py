import requests
from bs4 import BeautifulSoup
import json

# Replace with your actual API key and Custom Search Engine ID
API_KEY = 'AIzaSyBoG2B5sVAdRjuqsbufv9wWpB5nYOZXreY'
SEARCH_ENGINE_ID = '17466433701-m1s214i4ak9d3p15ibv45tjtrvm8t5cc.apps.googleusercontent.com'
QUERY = 'travel'

# Step 1: Use Google Custom Search API to search for "travel to Europe"
def google_search(query, api_key, search_engine_id):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={search_engine_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

search_results = google_search(QUERY, API_KEY, SEARCH_ENGINE_ID)

if search_results:
    items = search_results.get('items', [])
    urls = [item['link'] for item in items]

    # Step 2: Fetch and parse each URL
    for url in urls:
        print(f"Fetching URL: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.content
            soup = BeautifulSoup(page_content, 'html.parser')

            # Example parsing: Extract all paragraphs
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                print(p.get_text())

            print("\n" + "="*80 + "\n")

else:
    print("Failed to retrieve search results")
