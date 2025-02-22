from flask import Flask, request, jsonify, render_template
import openai
import json

app = Flask(__name__, template_folder="templates")

# Set your OpenAI API key here
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# System prompt for AI
SYSTEM_PROMPT = "You are a helpful assistant for home remedies and first aid."

# Load the knowledge base
KB_FILE = "knowledge_base.json"
try:
    with open(KB_FILE, "r") as file:
        knowledge_base = json.load(file)
except FileNotFoundError:
    knowledge_base = {}

def get_kb_response(query):
    """Fetch response from the knowledge base if available."""
    return knowledge_base.get(query.lower(), None)

def chat_with_gpt(user_input):
    """Call OpenAI's API and return response."""
    try:
        response = openai.ChatCompletion.create(
            model="GPT-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"  # Return error message if API fails

@app.route("/")
def home():
    """Render the main chatbot interface."""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handle chatbot messages."""
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"response": "Error: Invalid input."}), 400

        user_input = data["message"]

        # Check if response exists in the knowledge base
        kb_response = get_kb_response(user_input)
        response = kb_response if kb_response else chat_with_gpt(user_input)

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"response": f"Internal Server Error: {str(e)}"}), 500

if __name__ == "_main_":
    app.run(debug=True)  # Enable debug mode for detailed error logs