from framework.aidevs_framework import *
from secrets.secrets import GPT35TURBO_API_URL, OPENAI_API_KEY


task_name = "whoami"
question = None
hints = "### WSKAZÓWKI: "
retry = 10
for attempt in range(retry):
    token = get_token(task_name=task_name)
    task = authenticate(token=token, question=question)
    current_hint = task["hint"]
    hints += f"\n{attempt + 1}. {current_hint}"
    print(f"Hints:\n{hints}")
####################################################################

    HEADERS = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "OpenAI-Python-Client"
    }
    messages = [
        {
            "role": "system",
            "content": f"Twoim zadaniem jest domyśleć się o jaką osobę chodzi bazując na liście wskazówek. Jeśli podane wskazówki są niewystarczające, żeby się domyśleć o jaką osobę chodzi to MUSISZ ZWRÓCIĆ 0 i nic więcej. Jeśłi wskazówki są wystarczające, żeby się domyśleć co to za osoba, to wtedy ZWRÓĆ IMIĘ I NAZWISKO TEJ POSTACI I NIC WIĘCEJ. NIE WOLNO CI ZGADYWAĆ JEŚLI NIE WIESZ! NIE WOLNO CI ZWRACAĆ LIST JAK NP. '1. Ta osoba jest mężczyzną ...'! ZACZEKAJ ZE ZGADNIĘCIEM AŻ DOSTANIESZ MINIMUM PIĘĆ (5) WSKAZÓWEK! JEŚŁI WSKAZÓWEK JEST MNIEJ NIŻ 5 LUB NIE WIESZ KIM JEST TA POSTAĆ TO ZWRÓĆ 0 I NIC WIĘCEJ! MUSISZ odpowiadać SUPER-KRÓTKO i SUPER-ZWIĘŹLE!"
        },
        {
            "role": "user",
            "content": f"{hints}"
        }
    ]
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages
    }
    response = requests.post(GPT35TURBO_API_URL, headers=HEADERS, json=payload)
    answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    print(f"Answer:\n{answer}")

####################################################################
    if not ("0" in answer or "Przepraszam" in answer or "więcej" in answer):
        solve_task(answer=answer, token=token)
        exit(0)
print(f"No answer found after {retry} retries and hints:\n{hints}")
