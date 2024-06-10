import requests
import os

OPENAI_API_KEY = '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'
PROXY_URL = os.getenv('PROXY_URL')  # Proxy URL with optional authentication

import requests

proxy = {
            'http': 'http://pcUWRp:FGGSP7@161.0.7.29:8000',
            'https': 'http://pcUWRp:FGGSP7@161.0.7.29:8000'
        }

print(proxy)
url = 'https://api.openai.com/v1/images/generations'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {OPENAI_API_KEY}',
}
data = {
    'prompt': 'A scenic view of mountains',
    'n': 1,
    'size': '1024x1024'
}

try:
    response = requests.post(url, headers=headers, json=data, proxies=proxy, verify=False)
    response.raise_for_status()
    print(response.json())
except requests.exceptions.HTTPError as http_err:
    print(f'HTTP error occurred: {http_err} - Response: {http_err.response.content}')
except Exception as err:
    print(f'Error: {err}')

