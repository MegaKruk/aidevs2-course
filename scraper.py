from framework.aidevs_framework import *
from secrets.secrets import GPT35TURBO_API_URL, OPENAI_API_KEY
from requests.exceptions import RequestException
import time


task_name = "scraper"
question = None

token = get_token(task_name=task_name)
task = authenticate(token=token, question=question)

####################################################################

txt_url = task["input"]
task_msg = task["msg"]
task_question = task["question"]
retry = 10
delay = 1
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
txt = None
try:
    for attempt in range(retry):
        response = requests.get(txt_url, headers=headers)
        if response.status_code == 200:
            txt = response.text
            print("200 OK")
            print(txt)
            break
        else:
            print(f"Attempt {attempt + 1} failed. Status code: {response.status_code}\nSleeping for {delay}...")
            time.sleep(delay)  # Incremental delay
            delay += 5
except RequestException as e:
    print(f"Error fetching the webpage: {e}")

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "OpenAI-Python-Client"
}

messages = [
    {
        "role": "system",
        "content": f"Your task is to answer the question based on context. You must answer in concise manner and without unnecessary comments. {task_msg}\n### CONTEXT: {txt}"
    },
    {
        "role": "user",
        "content": f"### QUESTION: {task_question}"
    }
]

payload = {
    "model": "gpt-3.5-turbo",
    "messages": messages
}

response = requests.post(GPT35TURBO_API_URL, headers=HEADERS, json=payload)
answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
print(answer)
####################################################################

solve_task(answer=answer, token=token)
