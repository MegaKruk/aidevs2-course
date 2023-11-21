from framework.aidevs_framework import *
from my_secrets.my_secrets import GPT_API_URL, OPENAI_API_KEY, QDRANT_URL
import datetime
import ast


task_name = "gnome"
question = None

token = get_token(task_name=task_name)
task = authenticate(token=token, question=question)

####################################################################

task_query = task["msg"]
print(f"task_query: {task_query}")
task_url = task["url"]
print(f"task_url: {task_url}")

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "OpenAI-Python-Client"
}
messages = [{
    "content": [
        {"text": f"{task_query}. Answer in 1 word ONLY. Example: 'czerwony'", "type": "text"},
        {"image_url": task_url, "type": "image_url"}
    ],
    "role": "user"
}]
payload = {
    "model": "gpt-4-vision-preview",
    "messages": messages
}
response = requests.post(GPT_API_URL, headers=HEADERS, json=payload)
answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()

print(f"answer:\n{answer}")

####################################################################

solve_task(answer=answer, token=token)
