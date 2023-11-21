from flask import Flask, request, jsonify
from framework.aidevs_framework import *
from my_secrets.my_secrets import GPT_API_URL, OPENAI_API_KEY

app = Flask(__name__)
conversation_context = [] # Global variable to store context


def context_to_string():
    conversation_context_str = ""
    for entry in conversation_context:
        conversation_context_str += f"- {entry}\n"
    return conversation_context_str


def answer_question(question):
    user_content = f"### PYTANIE: {question}"
    if len(conversation_context) > 0:
        user_content += f"\n### KONTEKST: \n{context_to_string()}"

    HEADERS = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "OpenAI-Python-Client"
    }
    messages = [
        {"role": "system", "content": "Odpowiadasz na PYTANIA ULTRA-krótko i ULTRA-zwięźle, najlepiej 1 słowem. "
                                      "Czasami dostaniesz KONTEKST, wtedy posłuź się widzą z niego aby odpowiedzieć na PYTANIE. "
                                      "Przykładowe PYTANIE: 'Nad jakim morzem leży Polska?' Idealna odpowiedź: 'Bałtyckie'"},
        {"role": "user", "content": user_content}
    ]
    payload = {
        "model": "gpt-4",
        "messages": messages
    }
    response = requests.post(GPT_API_URL, headers=HEADERS, json=payload)
    answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    print(f"answer:\n{answer}")
    return answer


def remember(info):
    conversation_context.append(info)
    return f"OK. Info '{info}' was saved to context"


@app.route('/', methods=['POST'])
def ask():
    try:
        # Extract question from JSON
        data = request.json
        print(f"data:\n{data}")
        question_or_info = data.get('question')
        if question_or_info.endswith("?"):
            # Use your function to get the answer
            answer = answer_question(question_or_info)
        else:
            # Add info to the context
            answer = remember(question_or_info)
        # Return the answer in the required JSON format
        return jsonify({"reply": answer})

    except Exception as e:
        # Handle exceptions (e.g., bad JSON)
        return jsonify({"reply": str(e)})


@app.route('/context')
def context():
    return context_to_string()


@app.route('/health')
def health():
    return "ownapi app is healthy"


@app.route('/clear_context', methods=['POST'])
def clear_context():
    try:
        conversation_context.clear()
        return "context cleared"
    except Exception as e:
        return f"error while clearing context: {e}"


if __name__ == '__main__':
    app.run(debug=True)
