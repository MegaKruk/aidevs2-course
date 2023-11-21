from framework.aidevs_framework import *
from my_secrets.my_secrets import OPENAI_API_KEY
import openai

task_name = "functions"
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
answer = {
    "name": "addUser",
    "description": "Adds user given name, surname and year of birth",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "User's name"
            },
            "surname": {
                "type": "string",
                "description": "User's surname",
            },
            "year": {
                "type": "integer",
                "description": "Year of birth, 4-digit int",
            }
        },
        "required": [
            "name", "surname", "year"
        ]
    }
}

####################################################################

solve_task(answer=answer, token=token)
