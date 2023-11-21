from flask import Flask, request, jsonify
from framework.aidevs_framework import *
from my_secrets.my_secrets import GPT35TURBO_API_URL, OPENAI_API_KEY

app = Flask(__name__)


def answer_question(question):
    HEADERS = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "OpenAI-Python-Client"
    }
    messages = [
        {"role": "system", "content": "Odpowiadasz na PYTANIA ULTRA-krótko i ULTRA-zwięźle, najlepiej 1 słowem. Przykładowe PYTANIE: 'Nad jakim morzem leży Polska?' Idealna odpowiedź: 'Morze Bałtyckie'"},
        {"role": "user", "content": f"### PYTANIE: {question}"}
    ]
    payload = {
        "model": "gpt-4",
        "messages": messages
    }
    response = requests.post(GPT35TURBO_API_URL, headers=HEADERS, json=payload)
    answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    print(f"answer:\n{answer}")
    return answer


@app.route('/', methods=['POST'])
def ask():
    try:
        # Extract question from JSON
        data = request.json
        print(f"data:\n{data}")
        question = data.get('question')

        # Use your function to get the answer
        answer = answer_question(question)

        # Return the answer in the required JSON format
        return jsonify({"reply": answer})

    except Exception as e:
        # Handle exceptions (e.g., bad JSON)
        return jsonify({"reply": str(e)})


@app.route('/health')
def health():
    return "ownapi app is healthy"


if __name__ == '__main__':
    app.run(debug=True)
