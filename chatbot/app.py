from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

# Function to load system instructions from a text file
def load_system_instructions(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

# Function to append chat history to a file
def append_to_chat_history(user_input, ai_response):
    with open('chat_history.txt', 'a', encoding='utf-8') as file:
        file.write(f'User: {user_input}\nAI: {ai_response}\n\n')

# Configure API key (preferably from environment variable)
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key not found in environment variables")

genai.configure(api_key=api_key)

# Create the model and load system instructions
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

instructions_file = "instructions.txt"
system_instructions = load_system_instructions(instructions_file)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=system_instructions,
)

# Serve index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Handle chat requests
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['user_input']
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [user_input + '\n'],
            },
        ]
    )
    response = chat_session.send_message(user_input)
    
if __name__ == '__main__':
    app.run(debug=True)
