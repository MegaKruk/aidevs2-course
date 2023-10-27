from framework.common_lib import *

task_name = "helloapi"

token = get_token(task_name)
data = authenticate(token)

extracted_cookie = data["cookie"]
if extracted_cookie:
    solve_task(extracted_cookie, token)
else:
    print("Cookie not found")
