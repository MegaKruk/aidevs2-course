from framework.aidevs_framework import *


task_name = "google"
question = None

token = get_token(task_name=task_name)
task = authenticate(token=token, question=question)

####################################################################

answer = "https://9b45eb31a2dd0314be56c42725f2b291.serveo.net"

####################################################################

solve_task(answer=answer, token=token)
