
import requests
import json
import traceback

url = "http://localhost:5000/api/bazi/calculate"
payload = {
    "birthDate": "1990-01-31",
    "birthHour": 3,
    "gender": "male"
}

print(f"Testing connectivity to {url}...")
try:
    response = requests.post(url, json=payload, timeout=60)
    print(f"Status Code: {response.status_code}")
    print("Response Headers:", response.headers)
    if response.status_code == 200:
        print("Response JSON Preview:", str(response.json())[:200])
        print("SUCCESS")
    else:
        print("Response Text:", response.text)
        print("FAILED")
except Exception as e:
    print("EXCEPTION OCCURRED:")
    traceback.print_exc()
