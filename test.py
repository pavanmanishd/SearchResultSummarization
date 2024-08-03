import requests
import json

url = "http://localhost:11434/api/generate"

body = {   "model": "llama3.1:8b",   "prompt":"Why is the sky blue?" }
headers = {
    'Content-Type': 'application/json'
}
res = requests.post(url, headers=headers, data=json.dumps(body))

res = str(res.content, encoding='utf-8')
for i in res.split('\n'):
    d = json.loads(i)
    if d["done"]:
        break
    print(d["response"], end="")
    # print(i, sep='\n')