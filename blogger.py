from framework.aidevs_framework import *
from secrets.secrets import GPT35TURBO_API_URL, OPENAI_API_KEY


task_name = "blogger"

token = get_token(task_name=task_name)
task = authenticate(token=token)

####################################################################
answers_list = []
HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "OpenAI-Python-Client"
}

def generate_text(chapter):
    messages = [
        {"role": "system", "content": "Jesteś asystentem piszącym bloga o gotowaniu."},
        {"role": "user",
         "content": f"Stwórz treść dla rozdziału o tytule: {chapter} dotyczącego przygotowywania pizzy Margherity. Rozdziały mają być BARDZO krótkie, maksymalnie 2 lub 3 zdania"}
    ]

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages
    }

    response = requests.post(GPT35TURBO_API_URL, headers=HEADERS, json=payload)
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()

def create_blog(chapters):
    for chapter in chapters:
        text = generate_text(chapter)
        print(f"Chapter: {chapter}\nText: {text}")
        answers_list.append(text)
    return {"answer": answers_list}

print(f"answers: \n{answers_list}")

chapters = task["blog"]
answer = create_blog(chapters)

####################################################################

solve_task(answer=answer["answer"], token=token)
