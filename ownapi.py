from framework.aidevs_framework import *
from my_secrets.my_secrets import GPT_API_URL, OPENAI_API_KEY, QDRANT_URL
import datetime
import ast


task_name = "ownapipro" #"ownapi"
question = None

token = get_token(task_name=task_name)
task = authenticate(token=token, question=question)

####################################################################

answer = "https://e1828fe967026c1cc86330adea240767.serveo.net"

####################################################################

solve_task(answer=answer, token=token)
