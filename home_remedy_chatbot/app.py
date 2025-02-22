import openai
import json
from flask import Flask, request, jsonify, render_template

# Load OpenAI API Key (Replace with your actual key)
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# Load Knowledge Base
KB_FILE = "knowledge_base.json"
def load_knowledge_base():
    with open(KB_FILE, "r") as file:
        return json.load(file)
knowledge_base = load_knowledge_base()

# Define System Prompt
SYSTEM_PROMPT = """
You are a health assistant specializing in home remedies and first aid.
You provide scientifically backed home treatments and first aid procedures in simple language.
If a query is beyond basic home care, advise seeking professional medical attention.
"""

def get_kb_response(query):
    return knowledge_base.get(query.lower(), None)

def chat_with_gpt(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )
    return response["choices"][0]["message"]["content"]

def chatbot_response(user_input):
    kb_response = get_kb_response(user_input)
    if kb_response:
        return kb_response
    return chat_with_gpt(user_input)

# Flask Web Server
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = chatbot_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
