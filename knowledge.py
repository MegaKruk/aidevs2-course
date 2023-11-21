from framework.aidevs_framework import *
from my_secrets.my_secrets import GPT_API_URL, OPENAI_API_KEY, QDRANT_URL


task_name = "knowledge"
question = None

token = get_token(task_name=task_name)
task = authenticate(token=token, question=question)

####################################################################

task_question = task["question"]
print(f"task question: {task_question}")
HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "OpenAI-Python-Client"
}

messages = [
    {"role": "system", "content": "Kategoryzujesz PYTANIA."},
    {"role": "user",
     "content": f"### Możliwe KATEGORIE: populacja, waluta, inne. \n### PYTANIE: {task_question}. \nOdpowiedz 1 słowem - jedną z możliwych KATEGORII. Przykładowe PYTANIE: 'Kto napisał Hamleta?' Idealna ODPOWIEDŹ: 'inne'"}
]

payload = {
    "model": "gpt-3.5-turbo",
    "messages": messages
}

response = requests.post(GPT_API_URL, headers=HEADERS, json=payload)
category = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
print(f"category: {category}")
answer = []
if category == "populacja":
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    response.raise_for_status()
    countries = response.json()
    filtered_countries = [
        {'państwo': country['name']['common'], 'populacja': country['population']}
        for country in countries
    ]
    messages = [
        {"role": "system", "content": "Odpowiadasz na PYTANIA dotyczące populacji na podstawie KONTEKSTU."},
        {"role": "user",
         "content": f"### KONTEKST (forma: JSON): {filtered_countries} \n### PYTANIE: {task_question}. \nOdpowiedz ULTRA-krótka i ULTRA-zwięźle na podstawie KONTEKSTU i niczego innego. Przykładowe PYTANIE: 'jaka jest populacja Hong Kongu?' Idealna ODPOWIEDŹ: '7500700'. NIE WOLNO ci brać danych z czegokolwiek innego niż z KONTEKSTU, nawet ze swojej wiedzy! Podpowiedź: nazwy państw w PYTANIU są po polsku, a w KONTEKSCIE po angielsku."}
    ]
    payload = {
        "model": "gpt-4",
        "messages": messages
    }
    response = requests.post(GPT_API_URL, headers=HEADERS, json=payload)
    answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip().replace(" ", "")
elif category == "waluta":
    url = "http://api.nbp.pl/api/exchangerates/tables/A"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    rates = data[0]["rates"]
    messages = [
        {"role": "system", "content": "Odpowiadasz na PYTANIA dotyczące kursu walut na podstawie KONTEKSTU."},
        {"role": "user",
         "content": f"### KONTEKST (forma: JSON): {rates} \n### PYTANIE: {task_question}. \nOdpowiedz ULTRA-krótka i ULTRA-zwięźle na podstawie KONTEKSTU i niczego innego. Przykładowe PYTANIE: 'jaki jest teraz kurs dolara?' Idealna ODPOWIEDŹ: '4.0327'. Podpowiedź: jeśli mowa o dolarze bez dopisku o jaki konkretnie dolar chodzi, to załóż, że chodzi o dolar amerykański."}
    ]
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages
    }
    response = requests.post(GPT_API_URL, headers=HEADERS, json=payload)
    answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
elif category == "inne":
    messages = [
        {"role": "system", "content": "Odpowiadasz na PYTANIA dotyczące wiedzy ogólnej"},
        {"role": "user",
         "content": f"### PYTANIE: {task_question}. \nOdpowiedz ULTRA-krótka i ULTRA-zwięźle, najlepiej jednym słowem lub kilkoma słowami. Przykładowe PYTANIE: 'kto napisał Hamleta?' Idealna ODPOWIEDŹ: 'William Shakespeare'"}
    ]
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages
    }
    response = requests.post(GPT_API_URL, headers=HEADERS, json=payload)
    answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
else:
    raise Exception(f"Unknown category: {category}")


print(answer)

####################################################################

solve_task(answer=answer, token=token)
