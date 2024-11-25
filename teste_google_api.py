import requests

def google_search(query):
  url = 'https://www.googleapis.com/customsearch/v1'
  params = {
    'key': 'YOUR_API_KEY',
    'cx': 'YOUR_SEARCH_ENGINE_ID',
    'q': query
  }
  response = requests.get(url, params=params)
  return response.json()

# Exemplo de uso
resultado = google_search("Qual a capital do Brasil?")
print(resultado['items'][0]['title'])  # Imprime o título do primeiro resultado