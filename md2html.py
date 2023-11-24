from framework.aidevs_framework import *


task_name = "md2html"
question = None

token = get_token(task_name=task_name)
task = authenticate(token=token, question=question)

####################################################################

answer = "https://8d9a163eb7f7171b03eca9cb7f349b4e.serveo.net/md2html"

####################################################################

solve_task(answer=answer, token=token)
