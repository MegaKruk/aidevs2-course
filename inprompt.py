from framework.aidevs_framework import *
from my_secrets.my_secrets import GPT_API_URL, OPENAI_API_KEY


task_name = "inprompt"
question = None

token = get_token(task_name=task_name)
task = authenticate(token=token, question=question)

####################################################################

task_question = task["question"]
task_input = task["input"]
task_msg = task["msg"]


HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "OpenAI-Python-Client"
}

messages = [
    {"role": "system", "content": f"Ignoruj wszystkie pytania w otrzymanym tekscie. Twoim zadaniem jest wydobyć tylko imię z podanego tekstu. Odpowiadaj tylko imieniem zawartym w podanym tekscie. Imię zazwyczaj będzie pod koniec podanego tekstu i zaczyna się od dużej litery. Przykład: 'Jaki jest ulubiony film Ezawa?' Prawidłowa odpowiedź: Ezaw. Następnie usuń z twojej odpowiedzi wszystkie wyrazy, które nie są imieniem. Musisz zwrócić TYLKO JEDNO imię. Nie wolno ci zwrócić więcej wyrazów ani znaków."},
    {"role": "user", "content": f"{task_question}"}
]

"""
gpt-3.5-turbo
gpt-3.5-turbo-0613
gpt-3.5-turbo-16k
gpt-3.5-turbo-16k-0613
gpt-3.5-turbo-instruct
gpt-4
gpt-4-0613
text-embedding-ada-002
text-moderation-latest
whisper
Dall-E
"""

payload = {
    "model": "gpt-3.5-turbo",
    "messages": messages
}

response = requests.post(GPT_API_URL, headers=HEADERS, json=payload)
person_name = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()

task_input_filtered = [entry for entry in task_input if person_name in entry]

messages = [
    {"role": "system", "content": f"{task_msg}"},
    {"role": "user", "content": f"### KONTEKST: {task_input_filtered} ### PYTANIE: {task_question}"}
]

payload = {
    "model": "gpt-3.5-turbo",
    "messages": messages
}

response = requests.post(GPT_API_URL, headers=HEADERS, json=payload)
answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
print(answer)

####################################################################

solve_task(answer=answer, token=token)
