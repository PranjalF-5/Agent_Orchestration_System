import requests
import time
import json

url = "http://127.0.0.1:8000/tasks/"
payload = {
    "prompt": "Go to https://example.com and extract the exact text of the main heading (h1). Use browser_action.",
    "tenant_id": "test_user",
    "config": {}
}
headers = {
    "Content-Type": "application/json"
}

print(f"Sending POST request to {url}...")
start_time = time.time()

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Time: {time.time() - start_time:.2f} seconds")
    
    try:
        data = response.json()
        print("\n--- Response Data ---")
        print(json.dumps(data, indent=2))
    except json.JSONDecodeError:
        print("\n--- Raw Response Text ---")
        print(response.text)
        
except Exception as e:
    print(f"Request failed: {e}")
