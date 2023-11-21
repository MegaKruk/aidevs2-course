from framework.aidevs_framework import *
from my_secrets.my_secrets import GPT35TURBO_API_URL, OPENAI_API_KEY, QDRANT_URL
import datetime
import ast


task_name = "ownapi"
question = None

token = get_token(task_name=task_name)
task = authenticate(token=token, question=question)

####################################################################

answer = "https://527c36547591ad4adc7e9a6925e4e73d.serveo.net"

####################################################################

solve_task(answer=answer, token=token)
