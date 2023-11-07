from framework.common_lib import *
from secrets.secrets import GPT35TURBO_API_URL, OPENAI_API_KEY


task_name = "rodo"
question = None

token = get_token(task_name=task_name)
task = authenticate(token=token, question=question)

####################################################################

unflitered_text = task["msg"]

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "OpenAI-Python-Client"
}

content = "Take a deep breath and replace all personal data in the text with placeholder. DO NOT reword the original text in ways other than replacing personal data with placeholders. First name will be changed to %imie%. Surname will be changed to %nazwisko%. Profession will be changed to %zawod%. City will be changed %miasto%. Country will be changed to %panstwo%. "

####################################################################

solve_task(answer=content, token=token)
