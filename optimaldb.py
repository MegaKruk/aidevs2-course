from framework.aidevs_framework import *


task_name = "optimaldb"
question = None

token = get_token(task_name=task_name)
task = authenticate(token=token, question=question)

####################################################################

summarized_data = read_json_file("./data/optimized_3friends.json")
compressed_data = compress_data(summarized_data)
print(len(json.dumps(compressed_data).encode('utf-8')))

####################################################################

solve_task(answer=str(compressed_data), token=token)
