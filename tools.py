from framework.aidevs_framework import *
from my_secrets.my_secrets import GPT_API_URL, OPENAI_API_KEY, QDRANT_URL
import datetime
import ast


task_name = "tools"
question = None

token = get_token(task_name=task_name)
task = authenticate(token=token, question=question)

####################################################################

task_question = task["question"]
print(f"task question: {task_question}")

intentSchema = {
    "name": "describe_intention",
    "description": "",
    "parameters": {
        "type": "object",
        "properties": {
            "tool": {
                "type": "string",
                "description": """
                  tool musi być jednym z:
                  'ToDo' — zostanie wybrane kiedy użytkownik poprosi o zapamiętanie lub przypomnienie akcji do zrobienia przez niego na potem na czas nieokreślony. Przykład: 'Przypomnij mi, że mam kupić mleko' = {'tool': 'ToDo', 'desc': 'Kup mleko'}
                  'Calendar' — zostanie wybrane kiedy użytkownik poda informacje o nadchodzącym wydarzeniu, które można zapisać w kalendarzu w czasie określonym w PRZYSZŁOŚCI. Podpowiedź: jeśli mowa o dniu tygodnia np. o wtorku, i dzisiaj jest też wtorek, to chodzi o wtorek za 7 dni (w przyszłości). Przykład 1: 'Jutro mam spotkanie z Marianem' = {'tool': 'Calendar', 'desc': 'Spotkanie z Marianem', 'date': 'YYYY-MM-DD'}'. Przykład 2: 'Pojutrze mam kupić mleko' = {'tool': 'Calendar', 'desc': 'Kup mleko, 'date': 'YYYY-MM-DD'}'
                  """,
            }
        },
        "required": ["tool"],
    },
}

task_question = task["question"]

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "OpenAI-Python-Client"
}
messages = [
    {"role": "system", "content": f"{intentSchema}"},
    {"role": "user", "content": f" ### KONTEKST: dzisiaj jest {datetime.date.today()}l, pamiętaj, że chodzi o dzień tygodnia w PRZYSZŁOŚCI!\n ### ZAPYTANIE UŻYTKOWNIKA: {task_question}"}
]
payload = {
    "model": "gpt-4",
    "messages": messages
}
response = requests.post(GPT_API_URL, headers=HEADERS, json=payload)
intent = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
intent_dict = ast.literal_eval(intent)

print(f"intent:\n{intent_dict}")

####################################################################

solve_task(answer=intent_dict, token=token)
