from framework.aidevs_framework import *
from my_secrets.my_secrets import GPT_API_URL, OPENAI_API_KEY, QDRANT_URL
import datetime
import ast


task_name = "meme"
question = None

token = get_token(task_name=task_name)
task = authenticate(token=token, question=question)

####################################################################

task_image_url = task["image"]
task_text = task["text"]

result = generate_meme(task_text, task_image_url)
print(result)
answer = result["href"]

####################################################################

solve_task(answer=answer, token=token)
