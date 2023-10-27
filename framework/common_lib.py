import requests
from secrets.secrets import my_api_key


headers = {"Content-Type": "application/json"}

def get_token(task_name):
    response = requests.post(
        f"https://zadania.aidevs.pl/token/{task_name}",
        headers=headers,
        json={"apikey": my_api_key},
        verify=False
    )
    data = response.json()
    print(f"Response from get_token: \n{data}")
    if data.get("code") == 0:
        extracted_token = data["token"]
        return extracted_token
    else:
        print("Error in get_token")
        return None

def authenticate(token):
    response = requests.get(
        f"https://zadania.aidevs.pl/task/{token}",
        headers=headers,
        verify=False
    )
    data = response.json()
    if data.get("code") == 0:
        print(f"Response from authenticate: \n{data}")
    else:
        print(f"Authenticate returned error code {data.get('code')}: \n{data}")
    return data


def solve_task(answer, token):
    response = requests.post(
        f"https://zadania.aidevs.pl/answer/{token}",
        headers=headers,
        json={"answer": answer},
        verify=False
    )
    data = response.json()
    print(f"Response from answer: \n{data}")
    return data