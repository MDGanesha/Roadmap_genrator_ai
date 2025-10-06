import requests

url = "http://localhost:11434/api/generate"
prompt = {"model": "mistral", "prompt": "Give me a 3-week roadmap for learning Django"}
r = requests.post(url, json=prompt)
print(r.json())
