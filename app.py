from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
from chatbot_engine import ChatbotEngine

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Initialize chatbot engine
chatbot = ChatbotEngine()

@app.route('/')
def home():
    """Serve index.html"""
    return send_from_directory('.', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        personality = data.get('personality', 'friendly')
        
        if not user_message:

            return jsonify({'error': 'Empty message'}), 400
        
        # Get response from chatbot engine
        response = chatbot.get_response(user_message, personality)
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'version': '2.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """Get suggested questions"""
    suggestions = [
        "Namaste! Mujhe Python ke baare mein batao",
        "Web development kya hoti hai?",
        "Machine Learning kaise seekhoon?",
        "JavaScript kya hai?",
        "Data Science career guidance dedo",
        "API kya hota hai explain karo"
    ]
    return jsonify({'suggestions': suggestions})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
