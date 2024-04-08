import requests

def fetch_data(category, search_query=None):
    url = f"https://swapi.dev/api/{category}/"
    params = {}
    if search_query:
        params['search'] = search_query
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}