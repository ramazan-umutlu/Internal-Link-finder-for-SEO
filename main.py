import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

start = time.perf_counter()

session = requests.Session()
sitemap_response = session.get('YOUR_SITEMAP_URL')
sitemap_soup = BeautifulSoup(sitemap_response.content, 'lxml')
sitemap_urls = sitemap_soup.find_all("loc")

unique_urls = set()
for sitemap_url in sitemap_urls:
    unique_urls.add(sitemap_url.text)

search_terms = {
    'Your keyword1': False,
    'Your keyword2': False,
    'Your keyword3': False,
    'Your keyword4': False
}

results = []
for url in unique_urls:
    print(f'Requesting {url}')
    source_response = session.get(url)
    source_soup = BeautifulSoup(source_response.text, 'html.parser')

    for search_term in search_terms:
        search_terms[search_term] = bool(source_soup(text=re.compile(search_term)))

    results.append({
        'url': url,
        **search_terms
    })
print(results)
results_df = pd.DataFrame(results)
results_df.to_excel('YOUR_PATH/results.xlsx')

elapsed = time.perf_counter() - start
print(f'Time elapsed: {elapsed:0.6f} seconds')
