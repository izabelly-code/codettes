import requests
from bs4 import BeautifulSoup
import pandas as pd

API_KEY = ''
SEARCH_ENGINE_ID = ''
TIMEOUT = 15  
NUM_RESULTS = 10 

def google_search(query, api_key, search_engine_id, num_results, timeout):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={search_engine_id}&num={num_results}"
    response = requests.get(url, timeout=timeout)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve search results for query: {query} with status code {response.status_code}")
        return None

all_results = []

def run(query):
    search_results = google_search(query, API_KEY, SEARCH_ENGINE_ID, NUM_RESULTS, TIMEOUT)

    if search_results:
        items = search_results.get('items', [])
        urls = [item['link'] for item in items]

        for url in urls:
            print(f"Fetching URL: {url}")
            try:
                response = requests.get(url, timeout=TIMEOUT)
                if response.status_code == 200:
                    page_content = response.content
                    soup = BeautifulSoup(page_content, 'html.parser')

                    paragraphs = soup.find_all('p')
                    for p in paragraphs:
                        text = p.get_text()
                        all_results.append({'URL': url, 'Paragraph': text})

                    print("\n" + "="*80 + "\n")
                else:
                    print(f"Failed to fetch URL: {url} with status code {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Exception occurred while fetching URL: {url} - {e}")

    else:
        print("Failed to retrieve search results")

pesquisas_relacionadas = [
    "cursos mulheres na tecnologia",
    "vagas afirmativas para mulheres tecnologia",
    "vagas para mulheres trans tecnologia",
    "oportunidades de estágio para mulheres na tecnologia",
    "cursos online gratuitos para mulheres na tecnologia",
    "workshops para mulheres na programação",
    "comunidades de mulheres desenvolvedoras",
    "redes de networking para mulheres na tecnologia",
    "hackathons para mulheres",
]

for search in pesquisas_relacionadas:
    run(search)

df = pd.DataFrame(all_results)
df.drop_duplicates(subset=['URL', 'Paragraph'], inplace=True)

df.to_csv('search_results.csv', index=False, encoding='utf-8')
