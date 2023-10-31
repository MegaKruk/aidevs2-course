from framework.common_lib import *
from secrets.secrets import GPT35TURBO_API_URL, OPENAI_API_KEY


task_name = "liar"
question = "What is the highest mountain on Earth?"

token = get_token(task_name=task_name)
task = authenticate(token=token, question=question)

####################################################################

api_answer = task["answer"]

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "OpenAI-Python-Client"
}

messages = [
    {"role": "system", "content": "You are a fair arbiter that decides in a very precise manner whether "
                                  "provided ANSWER is on topic given provided QUESTION. Answer YES if ANSWER "
                                  "is on topic and answers the QUESTION and NO otherwise. Your answer must "
                                  "consist of a single WORD (YES or NO) - no other characters or words are "
                                  "acceptable in your answer"},
    {"role": "user",
     "content": f"### QUESTION: {question} ### ANSWER: {api_answer}"}
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
