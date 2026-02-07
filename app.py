import os
import requests
from flask import Flask, request, jsonify, Response, stream_with_context, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("API_KEY", "BW3g4tzjItnc9Wqimprh2sBvISrcEdLUzYnKaRuH")
API_URL = "https://api.cohere.ai/v1/chat"

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        message = data.get("message", "")
        history = data.get("history", [])

        system_directive = """
You are an AI Learning Assistant for Godavari Global University's Learning Management System (LMS). Your role is to help B.Tech CSE students with their coursework and academic queries.

**YOUR KNOWLEDGE BASE:**

1. **Data Structures (DS)** - Arrays, Linked Lists, Stacks, Queues, Trees, Graphs, Sorting, Searching algorithms
2. **Operating Systems (OS)** - Process management, Memory management, File systems, Scheduling, Deadlocks
3. **Environmental Studies (ES)** - Ecosystems, Biodiversity, Pollution, Climate change, Sustainability
4. **National Service Scheme (NSS)** - Community service, Social responsibility, Village camps, Environmental activities
5. **Life Skills (LS: PPHC)** - Communication, Leadership, Time management, Emotional intelligence
6. **Formal Languages & Automata Theory (FLAT)** - Regular expressions, Finite automata, Context-free grammars, Turing machines

**YOUR CAPABILITIES:**
- Answer questions about course topics with clear explanations
- Provide examples and practical applications
- Help with assignment concepts (not solutions)
- Explain complex topics in simple terms
- Guide students to relevant course materials
- Suggest study strategies and resources
- Remember student names and personal context shared during conversations
- Provide personalized learning support

**YOUR LIMITATIONS:**
- Do NOT provide complete assignment solutions or code
- Do NOT take exams or tests for students
- Do NOT access or modify student records

**YOUR TONE:**
- Professional yet friendly
- Patient and encouraging
- Clear and concise
- Academic but approachable
- Personalized when student shares their name or preferences
**RESPONSE FORMAT:**
- Keep responses focused and structured
- Use bullet points for clarity
- Provide examples when helpful
- Reference specific course units when relevant
- Address students by name when they've introduced themselves

Always prioritize student learning and academic integrity.
"""

        # Convert frontend history format to Cohere format
        chat_history = []
        for msg in history:
            if msg["role"] == "user":
                chat_history.append({"role": "USER", "message": msg["content"]})
            elif msg["role"] == "assistant":
                chat_history.append({"role": "CHATBOT", "message": msg["content"]})

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "command-r-08-2024",
            "message": message,
            "preamble": system_directive,
            "chat_history": chat_history,
            "temperature": 0.7
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            content = result['text']
            return jsonify({'response': content})
        else:
            return jsonify({'response': f"API Error: {response.status_code}"})

    except Exception as e:
        print("Error:", e)
        return jsonify({'response': f"Error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
