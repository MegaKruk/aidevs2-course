import requests


headers = {"Content-Type": "application/json"}
api_key = input("Enter your API key: ")

response = requests.post(
    "https://zadania.aidevs.pl/token/helloapi",
    headers=headers,
    json={"apikey": api_key},
    verify=False
)
data = response.json()
print(data)

if data.get("code") == 0:
    extracted_token = data["token"]
    response = requests.get(
        f"https://zadania.aidevs.pl/task/{extracted_token}",
        headers=headers,
        verify=False
    )
    data = response.json()
    print(data)
    if data.get("code") == 0:
        extracted_cookie = data["cookie"]
        if extracted_cookie:
            response = requests.post(
                f"https://zadania.aidevs.pl/answer/{extracted_token}",
                headers=headers,
                json={"answer": extracted_cookie},
                verify=False
            )
            data = response.json()
            print(data)
        else:
            print("Cookie not found")
    else:
        print("Error in second request")
else:
    print("Error in first request")
