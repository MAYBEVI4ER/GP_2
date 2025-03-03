import requests
import json
import pandas as pd
import time
from config import API_key

children_data = pd.read_csv("Childen_books_data.csv")

children_data

titles = children_data['Title'].dropna().tolist()

base_url = "https://www.googleapis.com/books/v1/volumes"
results = []

for title in titles:
    search_query = title.replace(' ', '+')
    url = f"{base_url}?q=intitle:{search_query}"
    flag = True
    while flag:
      try:
          response = requests.get(url, headers={'accept': 'application/json', 'X-API-KEY': API_key})
          if response.status_code == 200:
              flag = False
              response_data = response.json()

              if 'items' in response_data and len(response_data['items']) > 0:
                  first_result = response_data['items'][0]['volumeInfo']
                  results.append({
                      "Title": title,
                      "API Title": first_result.get('title'),
                      "Authors": first_result.get('authors', []),
                      "Publisher": first_result.get('publisher'),
                      "Published Date": first_result.get('publishedDate'),
                      "Description": first_result.get('description'),
                      "Page Count": first_result.get('pageCount'),
                      "Print Type": first_result.get('printType'),
                      "Categories": first_result.get('categories', []),
                      "Average Rating": first_result.get('averageRating'),
                      "Ratings Count": first_result.get('ratingsCount'),
                      "Language": first_result.get('language'),
                  })
              else:
                  results.append({
                      "Title": title,
                      "API Title": None,
                      "Authors": None,
                      "Publisher": None,
                      "Published Date": None,
                      "Description": None,
                      "Page Count": None,
                      "Print Type": None,
                      "Categories": None,
                      "Average Rating": None,
                      "Ratings Count": None,
                      "Language": None,
                  })
          else:
              print(f"Ошибка при запросе для '{title}': {response.status_code}")
              time.sleep(1)
      except Exception as e:
          print(f"Ошибка для '{title}': {e}")


    time.sleep(0.2)

results_df = pd.DataFrame(results)
results_df.to_csv("children_api_results.csv", index=False)