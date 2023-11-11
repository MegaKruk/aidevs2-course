from framework.aidevs_framework import *
from secrets.secrets import OPENAI_API_KEY
import openai

task_name = "whisper"
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

def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


task_msg = task["msg"]
audio_file_url = task["msg"].split(": ")[-1]
task_hint = task["hint"]

audio_file_path = download_file(audio_file_url)

audio_file = open(audio_file_path, "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file, api_key=OPENAI_API_KEY)
answer = transcript.text
print(answer)

####################################################################

solve_task(answer=answer, token=token)
