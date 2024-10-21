# How to run
- Use http proxy, not socks
- Use available OPENAI_API_KEY
- Use models based on its documentation

https://platform.openai.com/docs/guides/images/usage

```python
    prompt = data['prompt']

    # Refined prompt with more details
    refined_prompt = f"High-quality, detailed image of {prompt}, 4K resolution, photorealistic"

    url = 'https://api.openai.com/v1/images/generations'
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    json_data = {
        'prompt': refined_prompt,
        'n': 4,  # Number of images to generate
        'size': '1024x1024'
    }
    proxies = {
        'http': PROXY_URL,
        'https': PROXY_URL,
    } if PROXY_URL else None

    try:
        response = requests.post(url, headers=headers, json=json_data, proxies=proxies)
```
