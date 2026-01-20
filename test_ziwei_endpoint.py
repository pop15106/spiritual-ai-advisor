import requests
import json
import sys

url = 'http://localhost:5000/api/ziwei/calculate'
formatted_data = {
    'birthDate': '1990-01-01',
    'birthHour': 3
}

try:
    print(f"Sending POST to {url}...")
    response = requests.post(url, json=formatted_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text[:200]}")
    if response.status_code != 200:
        sys.exit(1)
except Exception as e:
    print(f"Request failed: {e}")
    sys.exit(1)
