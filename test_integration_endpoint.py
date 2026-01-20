import requests
import json
import sys

url = 'http://localhost:5000/api/integration/analyze'
data = {
    'question': '[用戶問題] 今年運勢如何？\n',
    'systems': ['tarot', 'ziwei', 'bazi'],
    'birth_data': {
        'date': '1990-01-01',
        'hour': 3,
        'gender': 'male'
    }
}

try:
    print(f"Sending POST to {url}...")
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success!")
        # print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
