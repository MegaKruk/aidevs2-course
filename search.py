from framework.aidevs_framework import *
from my_secrets.my_secrets import GPT_API_URL, OPENAI_API_KEY, QDRANT_URL


task_name = "search"
question = None

token = get_token(task_name=task_name)
task = authenticate(token=token, question=question)

####################################################################

QUERY = task["question"]
COLLECTION_NAME = "task_search_colection"
# JSON_FILE_PATH = "./data/archiwum.json"
#
# documents = read_json_file(JSON_FILE_PATH)
# create_collection_in_qdrant(COLLECTION_NAME, documents, QDRANT_URL, 'info')

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
    "with_vector": True
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

answer = search_results[("result")][0]["payload"]["url"]
print(answer)
####################################################################

solve_task(answer=answer, token=token)
