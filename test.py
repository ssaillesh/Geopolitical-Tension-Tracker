import requests

def test_api():
    url = "https://api.gdeltproject.org/api/v2/events/query"
    params = {
        'query': 'tariffs OR sanctions OR export ban',
        'format': 'json',
    }
    response = requests.get(url, params=params)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Sample Response:")
        print(response.json())  # Adjust this based on the response structure
    else:
        print("Failed to fetch data. Check API endpoint or parameters.")

test_api()
