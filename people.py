from framework.aidevs_framework import *
from my_secrets.my_secrets import GPT_API_URL, OPENAI_API_KEY, QDRANT_URL


task_name = "people"
question = None

token = get_token(task_name=task_name)
task = authenticate(token=token, question=question)

####################################################################

QUERY = task["question"]
COLLECTION_NAME = "task_people_colection"
# JSON_FILE_PATH = "./data/people.json"
#
# documents = read_json_file(JSON_FILE_PATH)
# doc_keys = ['imie', 'nazwisko', 'o_mnie', 'ulubiona_postac_z_kapitana_bomby', 'ulubiony_serial', 'ulubiony_film', 'ulubiony_kolor']
# create_collection_in_qdrant(COLLECTION_NAME, documents, QDRANT_URL, doc_keys)
# exit(0)
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}
embedding_payload = {
    "model": "text-embedding-ada-002",
    "input": QUERY
}
embedding_response = requests.post(ADA_002_API_URL, headers=headers, json=embedding_payload)
if embedding_response.status_code != 200:
    raise Exception(f"Error getting embedding: {embedding_response.json()}")

query_embedding = embedding_response.json().get("data", [{}])[0].get("embedding")
search_payload = {
    "vector": query_embedding,
    "limit": 1,
    "with_payload": True,
    "with_vector": True,
    # "filter": {
    #     "must": [
    #         {
    #             "key": 'source',
    #             "match": {
    #                 "value": COLLECTION_NAME
    #             }
    #         }
    #     ]
    # }
}
search_response = requests.post(f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points/search", json=search_payload)
if search_response.status_code != 200:
    raise Exception(f"Error searching in Qdrant: {search_response.json()}")

search_results = search_response.json()
context = ""
payload = search_results[("result")][0]["payload"]
for k, v in payload.items():
    if k in ['imie', 'nazwisko']:
        context += f"{v} "
    else:
        context += f"\n{k.replace('_', ' ').capitalize()}: {v}\n"
print(f"CONTEXT: \n{context}")

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "OpenAI-Python-Client"
}

messages = [
    {"role": "system", "content": "Odpowiadasz na PYTANIE na podstawie KONTEKSTU"},
    {"role": "user",
     "content": f"### KONTEKST: {context} \n### PYTANIE: {QUERY}. \nOdpowiedz na PYTANIE ULTRA-krótko i ULTRA-zwięźle. najlepiej 1 słowem. Odpowiadając na PYTANIE bierz pod uwagę TYLKO KONTEKST! Przykładowe PYTANIE: 'Jaki jest ulubiony kolor Mariusza Kaczki?' Przykładowy KONTEKST: 'Mariusz Kaczka ... Ulubiony kolor: malinowy' Idealna ODPOWIEDŹ: 'malinowy'"}
]

payload = {
    "model": "gpt-3.5-turbo",
    "messages": messages
}

response = requests.post(GPT_API_URL, headers=HEADERS, json=payload)
answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
print(f"ANSWER:{answer}")

####################################################################

solve_task(answer=context, token=token)
