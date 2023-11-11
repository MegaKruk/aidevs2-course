from framework.aidevs_framework import *
from secrets.secrets import MODERATION_API_ENDPOINT, OPENAI_API_KEY


task_name = "moderation"

token = get_token(task_name=task_name)
strings = authenticate(token=token)

####################################################################
answers = []
headers = {
    'Authorization': f'Bearer {OPENAI_API_KEY}',
    'Content-Type': 'application/json',
}

for sentence in strings["input"]:
    data = { 'input': sentence }

    response = requests.post(MODERATION_API_ENDPOINT, headers=headers, json=data)

    results = response.json().get('results', [])
    if results[0]["flagged"]:
        answers.append(1)
    else:
        answers.append(0)

print(f"answers: \n{answers}")

####################################################################

solve_task(answer=answers, token=token)
