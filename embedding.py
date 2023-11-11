from framework.aidevs_framework import *
from secrets.secrets import ADA_002_API_URL, OPENAI_API_KEY


task_name = "embedding"
question = None

token = get_token(task_name=task_name)
task = authenticate(token=token, question=question)


####################################################################

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

task_msg = task["msg"]
task_hint1 = task["hint1"]
task_hint2 = task["hint2"]
task_hint3 = task["hint3"]


HEADERS = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

payload = {
        "model": "text-embedding-ada-002",
        "input": f"Hawaiian pizza"
    }

response = requests.post(ADA_002_API_URL, headers=HEADERS, json=payload)
answer = []
if response.status_code == 200:
    answer = response.json().get("data", [{}])[0].get("embedding")
else:
    # Handle error
    response.raise_for_status()
print(f"Answer: \n{answer}")

####################################################################

solve_task(answer=answer, token=token)
